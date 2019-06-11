import hashlib
import json
import os
import shutil
import uuid

from flask import Flask, request, Response

from compiler import Compiler
from config import (JUDGER_WORKSPACE_BASE, SPJ_SRC_DIR, SPJ_EXE_DIR, COMPILER_USER_UID, SPJ_USER_UID,
                    RUN_USER_UID, RUN_GROUP_GID, TEST_CASE_DIR)
from exception import TokenVerificationFailed, CompileError, SPJCompileError, JudgeClientError
from judge_client import JudgeClient
from utils import server_info, logger, token, ProblemIOMode

app = Flask(__name__)
DEBUG = os.environ.get("judger_debug") == "1"
app.debug = DEBUG


class InitSubmissionEnv(object):
    def __init__(self, judger_workspace, submission_id, init_test_case_dir=False):
        self.work_dir = os.path.join(judger_workspace, submission_id)
        self.init_test_case_dir = init_test_case_dir
        if init_test_case_dir:
            self.test_case_dir = os.path.join(self.work_dir, "submission_" + submission_id)
        else:
            self.test_case_dir = None

    def __enter__(self):
        try:
            os.mkdir(self.work_dir)
            if self.init_test_case_dir:
                os.mkdir(self.test_case_dir)
            os.chown(self.work_dir, COMPILER_USER_UID, RUN_GROUP_GID)
            os.chmod(self.work_dir, 0o711)
        except Exception as e:
            logger.exception(e)
            raise JudgeClientError("failed to create runtime dir")
        return self.work_dir, self.test_case_dir

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not DEBUG:
            try:
                shutil.rmtree(self.work_dir)
            except Exception as e:
                logger.exception(e)
                raise JudgeClientError("failed to clean runtime dir")


class JudgeServer:
    @classmethod
    def ping(cls):
        data = server_info()
        data["action"] = "pong"
        return data

    @classmethod
    def judge(cls, language_config, src, max_cpu_time, max_memory, test_case_id=None, test_case=None,
              spj_version=None, spj_config=None, spj_compile_config=None, spj_src=None, output=False,
              io_mode=None):
        if not io_mode:
            io_mode = {"io_mode": ProblemIOMode.standard}

        if not (test_case or test_case_id) or (test_case and test_case_id):
            raise JudgeClientError("invalid parameter")
        # init
        compile_config = language_config.get("compile")
        run_config = language_config["run"]
        submission_id = uuid.uuid4().hex

        is_spj = spj_version and spj_config

        if is_spj:
            spj_exe_path = os.path.join(SPJ_EXE_DIR, spj_config["exe_name"].format(spj_version=spj_version))
            # spj src has not been compiled
            if not os.path.isfile(spj_exe_path):
                logger.warning("%s does not exists, spj src will be recompiled")
                cls.compile_spj(spj_version=spj_version, src=spj_src,
                                spj_compile_config=spj_compile_config)

        init_test_case_dir = bool(test_case)
        with InitSubmissionEnv(JUDGER_WORKSPACE_BASE, submission_id=str(submission_id), init_test_case_dir=init_test_case_dir) as dirs:
            submission_dir, test_case_dir = dirs
            test_case_dir = test_case_dir or os.path.join(TEST_CASE_DIR, test_case_id)

            if compile_config:
                src_path = os.path.join(submission_dir, compile_config["src_name"])

                # write source code into file
                with open(src_path, "w", encoding="utf-8") as f:
                    f.write(src)
                os.chown(src_path, COMPILER_USER_UID, 0)
                os.chmod(src_path, 0o400)

                # compile source code, return exe file path
                exe_path = Compiler().compile(compile_config=compile_config,
                                              src_path=src_path,
                                              output_dir=submission_dir)
                try:
                    # Java exe_path is SOME_PATH/Main, but the real path is SOME_PATH/Main.class
                    # We ignore it temporarily
                    os.chown(exe_path, RUN_USER_UID, 0)
                    os.chmod(exe_path, 0o500)
                except Exception:
                    pass
            else:
                exe_path = os.path.join(submission_dir, run_config["exe_name"])
                with open(exe_path, "w", encoding="utf-8") as f:
                    f.write(src)

            if init_test_case_dir:
                info = {"test_case_number": len(test_case), "spj": is_spj, "test_cases": {}}
                # write test case
                for index, item in enumerate(test_case):
                    index += 1
                    item_info = {}

                    input_name = str(index) + ".in"
                    item_info["input_name"] = input_name
                    input_data = item["input"].encode("utf-8")
                    item_info["input_size"] = len(input_data)

                    with open(os.path.join(test_case_dir, input_name), "wb") as f:
                        f.write(input_data)
                    if not is_spj:
                        output_name = str(index) + ".out"
                        item_info["output_name"] = output_name
                        output_data = item["output"].encode("utf-8")
                        item_info["output_md5"] = hashlib.md5(output_data).hexdigest()
                        item_info["output_size"] = len(output_data)
                        item_info["stripped_output_md5"] = hashlib.md5(output_data.rstrip()).hexdigest()

                        with open(os.path.join(test_case_dir, output_name), "wb") as f:
                            f.write(output_data)
                    info["test_cases"][index] = item_info
                with open(os.path.join(test_case_dir, "info"), "w") as f:
                    json.dump(info, f)

            judge_client = JudgeClient(run_config=language_config["run"],
                                       exe_path=exe_path,
                                       max_cpu_time=max_cpu_time,
                                       max_memory=max_memory,
                                       test_case_dir=test_case_dir,
                                       submission_dir=submission_dir,
                                       spj_version=spj_version,
                                       spj_config=spj_config,
                                       output=output,
                                       io_mode=io_mode)
            run_result = judge_client.run()

            return run_result

    @classmethod
    def compile_spj(cls, spj_version, src, spj_compile_config):
        spj_compile_config["src_name"] = spj_compile_config["src_name"].format(spj_version=spj_version)
        spj_compile_config["exe_name"] = spj_compile_config["exe_name"].format(spj_version=spj_version)

        spj_src_path = os.path.join(SPJ_SRC_DIR, spj_compile_config["src_name"])

        # if spj source code not found, then write it into file
        if not os.path.exists(spj_src_path):
            with open(spj_src_path, "w", encoding="utf-8") as f:
                f.write(src)
            os.chown(spj_src_path, COMPILER_USER_UID, 0)
            os.chmod(spj_src_path, 0o400)

        try:
            exe_path = Compiler().compile(compile_config=spj_compile_config,
                                          src_path=spj_src_path,
                                          output_dir=SPJ_EXE_DIR)
            os.chown(exe_path, SPJ_USER_UID, 0)
            os.chmod(exe_path, 0o500)
        # turn common CompileError into SPJCompileError
        except CompileError as e:
            raise SPJCompileError(e.message)
        return "success"


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=["POST"])
def server(path):
    if path in ("judge", "ping", "compile_spj"):
        _token = request.headers.get("X-Judge-Server-Token")
        try:
            if _token != token:
                raise TokenVerificationFailed("invalid token")
            try:
                data = request.json
            except Exception:
                data = {}
            ret = {"err": None, "data": getattr(JudgeServer, path)(**data)}
        except (CompileError, TokenVerificationFailed, SPJCompileError, JudgeClientError) as e:
            logger.exception(e)
            ret = {"err": e.__class__.__name__, "data": e.message}
        except Exception as e:
            logger.exception(e)
            ret = {"err": "JudgeClientError", "data": e.__class__.__name__ + " :" + str(e)}
    else:
        ret = {"err": "InvalidRequest", "data": "404"}
    return Response(json.dumps(ret), mimetype='application/json')


if DEBUG:
    logger.info("DEBUG=ON")

# gunicorn -w 4 -b 0.0.0.0:8080 server:app
if __name__ == "__main__":
    app.run(debug=DEBUG)
