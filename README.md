## 安装基础环境

以下命令都需要 root 用户身份运行，请自行添加 `sudo`

 - 必要的工具 `apt-get update && apt-get install -y vim python-pip curl git`
 - 安装 docker `curl -sSL https://get.daocloud.io/docker | sh`
 - 安装 docker-compose `LC_CTYPE= pip install docker-compose`

## 准备安装文件

请选择磁盘空间富余的位置，运行下面的命令

`git clone https://github.com/QingdaoU/OnlineJudgeDeploy.git && cd OnlineJudgeDeploy`

然后编辑 `docker-compose.yml` 第28行为自定义的密码，比如`rpc_token=123456`

## 启动服务

运行 `docker-compose up -d` ，不需要其他的步骤，大约一分钟之后 web 界面就可以访问了，默认开放80和443端口。其中443端口是自签名证书。

注意，对于非root用户，请用 `sudo -E docker-compose up -d`，否则不会传递当前的 `$PWD` 环境变量。

## 这就结束了

超级管理员用户名是root，默认密码是`password@root`，请及时修改。

登录`/admin`，添加一个判题服务器，地址为`judger`，端口为`8080`，密码是上面自定义的`rpc_token`。

修改`custom_settings.py`可以自定义站点信息。
