## Linux 系统安装基础环境

以 Ubuntu 为例，其他可以安装 Docker 的系统也可以。

以下命令都需要 root 用户身份运行，请自行添加 `sudo`

- 必要的工具 `apt-get update && apt-get install -y vim python-pip curl git`
- 安装 Docker `curl -sSL https://get.daocloud.io/docker | sh` （这一步可能比较慢，请耐心等待，官方的安装指南见 https://docs.docker.com/engine/installation/ ）
- 安装 docker-compose `pip install docker-compose`

## Windows 系统安装基础环境

Windows 下仅用临时的测试，不要在生产环境使用 Docker for Windows。

以下教程仅适用于 Win10 x64 下的 `PowerShell`

- 安装 Windows 的 Docker 工具
- 右击右下角 Docker 图标，选择 Settings 进行设置
- 选择 `Shared Drives` 菜单，之后勾选你想安装 OJ 的盘符位置（例如勾选D盘），点击 `Apply`
- 输入 Windows 的账号密码进行文件共享
- 启动 `PowerShell`，输入`$env:PWD='{your path}'`. `{your path}`代表你想安装的目录。注意！目录必须在你共享的盘符中（例如设置`D:\qduoj`）。由于你创建的是临时环境变量，`PowerShell`关闭则临时变量作废，因此每次启动前必须重新设置过。当然你也可以选择在Win的环境变量中永久添加名为`PWD`的环境变量（与JDK设置方法相同）

>在Windows上面运行 Docker 实际上通过 `Hyper-V` 新建了一个 Linux 虚拟机，然后在虚拟机里面运行Docker。因此目录的挂载需要进行文件共享设置。`docker-compose.yml` 里面 `volumes` 挂载目录写的是 `$PWD`，这个在 Linux 里面代表当前目录，而 Windows 中默认不存在。

## 准备安装文件

请选择磁盘空间富余的位置，依次运行下面的命令

```bash
git clone -b 2.0 https://github.com/QingdaoU/OnlineJudgeDeploy.git && cd OnlineJudgeDeploy
```

## 启动服务

```bash
docker-compose up -d
```

> 对于非root用户，请用 `sudo -E docker-compose up -d`，否则不会传递当前的 `$PWD` 环境变量。

根据网速情况，大约5到30分钟就可以自动搭建完成，全程无需人工干预。

等命令执行完成，然后运行 `docker ps -a`，看到所有的容器的状态没有 `unhealthy` 或 `Exited (x) xxx` 就代表容器启动成功。然后 `docker logs -f oj-backend` 直到看到 `XX entered RUNNING state, process has stayed up for > than 5 seconds (startsecs)` 就可以 `ctrl + c` 结束掉了，代表已经安装成功。

## 尽情享用吧

通过浏览器访问服务器的 HTTP 80 端口或者 HTTPS 443 端口，就可以开始使用了。后台管理路径为`/admin`, 安装过程中自动添加的超级管理员用户名为`root`，密码为`rootroot`， **请务必及时修改密码**。

不要忘记阅读文档 http://docs.onlinejudge.me/

## 定制

2.0版将一些常用设置放到了后台管理中，您可以直接登录管理后台对系统进行配置，而无需进行代码改动。

若需要对系统进行修改或二次开发，请参照各模块的**README**，修改完成后需自行构建Docker镜像并修改`docker-compose.yml`

## 遇到了问题？

请参照: [http://docs.onlinejudge.me/](http://docs.onlinejudge.me/#/onlinejudge/faq) ，如有其他问题请入群讨论或提issue。
