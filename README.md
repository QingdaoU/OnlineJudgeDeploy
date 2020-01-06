# QDUOJ Docker 镜像部署文档

## 环境准备

### Linux 环境

1. 安装必要的依赖

    - 如果apt速度慢请参阅[FAQ](./doc/faq.md#安装依赖组件超时或速度慢)

    ```bash
    sudo apt-get update
    sudo apt-get install -y vim python3-pip curl git
    sudo pip3 install docker-compose -i https://pypi.tuna.tsinghua.edu.cn/simple
    # 注意：国外服务器直接sudo pip3 install docker-compose即可，不需要指定软件源。
    # 验证安装
    docker-compose version
    # docker-compose version 1.25.0, build 1110ad01
    ```

    - 注意：pip更新后如果出现`Cannot import name "main"`请参阅[此处](./doc/pip-cannot-import-name-main.md)

    - 执行`docker-compose version`时如提示找不到文件，请参阅[此处](./doc/cannot-find-docker-compose.md)

2. 安装 Docker 

    - 使用一键脚本

        - 国内服务器

        ```bash
        curl -fsSL https://get.daocloud.io/docker -o get-docker.sh
        sudo sh get-docker.sh --mirror Aliyun
        sudo service docker start
        ```

        - 国外服务器

        ```bash
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        sudo service docker start
        ```

        - 注意：Docker并不推荐在生产环境中使用一键脚本安装（参阅[链接](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-convenience-script)）

    - 分步安装

        - 请参阅：

            - [在Ubuntu服务器上安装Docker CE和docker-compose](./doc/ubuntu-docker-installation.md)

            - [Docker官网](https://docs.docker.com/install/)

3. 配置非root用户运行

    - 如果需要非root用户也能运行docker（例如运维不开放root用户），请参阅[FAQ](./doc/faq.md#配置非root用户运行)

    - 注意：将非root添加至`docker`用户组后，由该用户运行的容器仍可获得root权限，可能会有一定安全隐患。[参阅](https://docs.docker.com/engine/security/security/#docker-daemon-attack-surface)

4. 国内服务器配置Docker镜像源

    - 参阅[FAQ](./doc/faq.md#国内服务器配置阿里云Docker镜像仓库)

5. 安装Docker时的常见问题

    - 参阅[FAQ](./doc/faq.md)

    - 问题列表：

        - 安装依赖组件超时或速度慢

        - 国内服务器安装Docker超时或速度慢

        - Docker pull 或 docker-compose pull 超时速度慢

        - 安装docker-compose后运行提示/usr/bin/docker-compose: No such file or directory

        - Couldn't connect to Docker daemon at ... - is it running?

        - 配置非root用户运行

        - 国内服务器配置阿里云Docker镜像仓库

### Windows 环境


Windows 下的安装仅供体验，勿在生产环境使用。如有必要，请使用虚拟机安装 Linux 并将 OJ 安装在其中。

以下教程仅适用于 Win10 x64 下的 `PowerShell`

1. 安装 Windows 的 Docker 工具
2. 右击右下角 Docker 图标，选择 Settings 进行设置
3. 选择 `Shared Drives` 菜单，之后勾选你想安装 OJ 的盘符位置（例如勾选D盘），点击 `Apply`
4. 输入 Windows 的账号密码进行文件共享
5. 安装 `Python`、`pip`、`git`、`docker-compose`，安装方法自行搜索。

## 开始安装

1. 请选择磁盘空间富余的位置，运行下面的命令

    ```bash
    git clone -b 2.0 https://github.com/QingdaoU/OnlineJudgeDeploy.git && cd OnlineJudgeDeploy
    ```

2. 启动服务

    ```bash
    docker-compose up -d
    ```

根据网速情况，大约5到30分钟就可以自动搭建完成，全程无需人工干预。

等命令执行完成，然后运行 `docker ps -a`，当看到所有的容器的状态没有 `unhealthy` 或 `Exited (x) xxx` 就代表 OJ 已经启动成功。

## 尽情享用吧

通过浏览器访问服务器的 HTTP 80 端口或者 HTTPS 443 端口，就可以开始使用了。后台管理路径为`/admin`, 安装过程中自动添加的超级管理员用户名为 `root`，密码为 `rootroot`， **请务必及时修改密码**。

不要忘记阅读文档 http://docs.onlinejudge.me/

## 定制

2.0 版将一些常用设置放到了后台管理中，您可以直接登录管理后台对系统进行配置，而无需进行代码改动。

若需要对系统进行修改或二次开发，请参照各模块的**README**，修改完成后需自行构建Docker镜像并修改`docker-compose.yml`

## 遇到了问题？

请参照: [http://docs.onlinejudge.me/](http://docs.onlinejudge.me/#/onlinejudge/faq) ，如有其他问题请入群讨论或提issue。
