import _judger
import json
import os

from config import COMPILER_LOG_PATH, COMPILER_USER_UID, COMPILER_GROUP_GID
from exception import CompileError


class Compiler(object):
    def compile(self, compile_config, src_path, output_dir):
        command = compile_config["compile_command"]
        exe_path = os.path.join(output_dir, compile_config["exe_name"])
        command = command.format(src_path=src_path, exe_dir=output_dir, exe_path=exe_path)
        compiler_out = os.path.join(output_dir, "compiler.out")
        _command = command.split(" ")

        os.chdir(output_dir)
        result = _judger.run(max_cpu_time=compile_config["max_cpu_time"],
                             max_real_time=compile_config["max_real_time"],
                             max_memory=compile_config["max_memory"],
                             max_stack=128 * 1024 * 1024,
                             max_output_size=1024 * 1024,
                             max_process_number=_judger.UNLIMITED,
                             exe_path=_command[0],
                             # /dev/null is best, but in some system, this will call ioctl system call
                             input_path=src_path,
                             output_path=compiler_out,
                             error_path=compiler_out,
                             args=_command[1::],
                             env=["PATH=" + os.getenv("PATH")],
                             log_path=COMPILER_LOG_PATH,
                             seccomp_rule_name=None,
                             uid=COMPILER_USER_UID,
                             gid=COMPILER_GROUP_GID)

        if result["result"] != _judger.RESULT_SUCCESS:
            if os.path.exists(compiler_out):
                with open(compiler_out, encoding="utf-8") as f:
                    error = f.read().strip()
                    os.remove(compiler_out)
                    if error:
                        raise CompileError(error)
            raise CompileError("Compiler runtime error, info: %s" % json.dumps(result))
        else:
            os.remove(compiler_out)
            return exe_path
