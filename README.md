## Linux 系统安装基础环境

以下命令都需要 root 用户身份运行，请自行添加 `sudo`

 - 必要的工具 `apt-get update && apt-get install -y vim python-pip curl git`
 - 安装 docker `curl -sSL https://get.daocloud.io/docker | sh`
 - 安装 docker-compose `pip install docker-compose`

## Windows 系统安装基础环境

Windows 下面安装会有很多坑，经过测试时，Win10 x64下的 `PowerShell` 可以正常使用。

- 安装 Windows 的 Docker 工具
- 右击右下角 Docker 图标，选择 Settings 进行设置
- 选择 `Shared Drives` 菜单，之后勾选你想安装 OJ 的盘符位置（例如勾选D盘），点击 `Apply`
- 输入 Windows 的账号密码进行文件共享
- 启动 `PowerShell`，输入`$env:PWD='{your path}'，{you path}`代表你想安装的目录。注意！目录必须在你共享的盘符中（例如设置`D:\qduoj`）。由于你创建的是临时环境变量，`PowerShell`关闭则临时变量作废，因此每次启动前必须重新设置过。当然你也可以选择在Win的环境变量中永久添加名为`PWD`的环境变量（与JDK设置方法相同）

### 注意
 - 因为 Docker 使用了很多 Linux 的特性，所以 Windows上面运行 Docker 实际上通过 `Hyper-V` 新建了一个 Linux 虚拟机，然后在虚拟机里面运行Docker。因此目录的挂载需要进行文件共享设置。`docker-compose.yml` 里面 `volumes` 挂载目录写的是 `$PWD`，这个在 Linux 里面代表当前目录，而 Windows 中默认不存在。

## 准备安装文件

请选择磁盘空间富余的位置，运行下面的命令

```sh
git clone https://github.com/QingdaoU/OnlineJudgeFE.git
git clone -b 2.0 https://github.com/QingdaoU/OnlineJudge.git
git clone -b 2.0 https://github.com/QingdaoU/OnlineJudgeDeploy.git
cd OnlineJudgeDeploy
```

然后编辑 `docker-compose.yml` 将41行的`JUDGE_SERVER_TOKEN`和第68行的`TOKEN`修改为自定义的值， 两处值必须相同且`=`前后不能有空格

## 启动服务

运行 `docker-compose up -d` 根据网速情况，大约5到30分钟就可以自动搭建完成，全程无需人工干预。
若想获悉安装进度，运行`docker-compose logs`查看安装日志，当显示结果中出现以下文字时
```
Congratulations, All have done without error.
```
表示安装已成功结束

注意，对于非root用户，请用 `sudo -E docker-compose up -d`，否则不会传递当前的 `$PWD` 环境变量。

## 尽情享用吧

通过浏览器访问服务器的80端口，就可以开始使用了
后台管理默认路径为`/admin`, 安装过程中自动添加的超级管理员用户名为`root`，密码为`rootroot`， 请务必及时修改。
