## 非Windows安装基础环境

以下命令都需要 root 用户身份运行，请自行添加 `sudo`

 - 必要的工具 `apt-get update && apt-get install -y vim python-pip curl git`
 - 安装 docker `curl -sSL https://get.daocloud.io/docker | sh`
 - 安装 docker-compose `LC_CTYPE= pip install docker-compose`

## Windows安装必看

Windows下面安装会有很多坑，本人使用Win10的`PowerShell`测试成功

- 安装Windows的docker工具
- 右击右下角docker图标，选择Settings进行设置
- 选择`Shared Drives`菜单，之后勾选你想安装OJ的盘符位置（例如我勾选了D盘），点击Apply
- 输入Windows的账号密码进行文件共享
- 设置`PWD`(大小写没试过，我是大写的)的环境变量为你想安装的目录，注意！目录必须在你共享的盘符中（例如我设置的是`D:\qdoj`）
- 完成

> 接下来我简单的介绍下为什么Win下面的Docker为什么这么麻烦。因为Docker使用了很多Linux的特性，所以windows上面运行Docker实际上通过`hyper-v`新建了一个Linux虚拟机，然后在虚拟机里面运行Docker。
因此目录的挂载需要进行文件共享设置。然后`docker-compose.yml`里面`volumes`挂载目录写的是`$PWD`，这个在Linux里面代表当前目录，而Win中指的是`PWD`这个环境变量，如果你细心的话你会发现安装的时候它会
提示`PWD`不存在，默认使用`/`。结果这个目录就被挂载到了虚拟机中去了，所以Win上面看不见你挂载的目录。

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
