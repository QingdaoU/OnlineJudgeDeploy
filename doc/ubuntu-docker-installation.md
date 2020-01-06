# Ubuntu服务器安装Docker和docker-compose

> 原文：https://docs.docker.com/install/linux/docker-ce/ubuntu/
> 
> 加入了阿里云Docker软件源和镜像仓库

0. 首先确保运行的是以下几个版本之一：

    - Disco 19.04

    - Cosmic 18.10

    - Bionic 18.04 (LTS)

    - Xenial 16.04 (LTS)

    - 如果运行的是Ubuntu 14.04，请参考[这里](https://docs.docker.com/v18.03/install/linux/docker-ce/ubuntu/)安装Docker 18.03。

    > 注意：所有安装操作均须root权限，如果不是root用户，命令前面的`sudo`不能省略。

1. 卸载旧版Docker及相关软件包

    ```bash
    sudo apt-get remove -y docker docker-engine docker.io containerd runc
    ```

2. 更新软件源

    ```bash
    sudo apt-get update
    ```

    - 如果apt速度慢请参阅[FAQ](./faq.md#安装依赖组件超时或速度慢)

3. 安装依赖组件

    ```bash
    sudo apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg-agent \
        software-properties-common
    ```

4. 添加GPG密钥和软件源（国内服务器请跳至步骤5）

    ```bash
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    ```
    - **如果是国内服务器请参阅步骤5的替代软件源**

    - 验证密钥

    ```bash
    sudo apt-key fingerprint 0EBFCD88
    ```

    > 出现类似如下的字样说明密钥添加成功

        pub   rsa4096 2017-02-22 [SCEA]
            9DC8 5822 9FC7 DD38 854A  E2D8 8D81 803C 0EBF CD88
        uid           [ unknown] Docker Release (CE deb) <docker@docker.com>
        sub   rsa4096 2017-02-22 [S]

    - 添加软件源（国内服务器请跳过此步骤）

    ```bash
    sudo add-apt-repository \
        "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) \
        stable"
    ```

5. 国内服务器添加GPG密钥和软件源（国外服务器请跳至步骤6）

    ```bash
    curl -fsSL http://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -

    sudo add-apt-repository "deb [arch=amd64] http://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
    ```

    - 如果是阿里云服务器，可以直接使用内网软件源，无需采用上面的源：

    ```bash
    # 经典网络
    curl -fsSL http://mirrors.aliyuncs.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] http://mirrors.aliyuncs.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
    # VPC网络
    curl -fsSL http://mirrors.cloud.aliyuncs.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] http://mirrors.cloud.aliyuncs.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
    ```

6. 更新软件源

    ```bash
    sudo apt-get update
    ```

7. 安装Docker CE

    ```bash
    sudo apt-get install docker-ce docker-ce-cli containerd.io
    ```

8. 国内服务器配置Docker镜像源（国外服务器请跳过）

    - 参阅[FAQ](./faq.md#国内服务器配置阿里云Docker镜像仓库)

9. 验证Docker安装

    ```bash
    sudo docker run hello-world
    # 显示Hello from Docker!字样即为成功运行
    ```

    - 验证后，可以通过`sudo docker rm $(docker ps -aq); sudo docker rmi hello-world`删除`hello-world`镜像（前半句命令会删除本机的所有docker容器，请确保没有其他重要容器存在，如有请使用`sudo docker ps -a`找到`hello-world`容器并执行`sudo docker rm ${容器ID}`手动删除该容器。

10. 安装 `docker-compose`

    ```bash
    sudo curl -L "https://github.com/docker/compose/releases/download/1.25.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

    # 赋予执行权限
    sudo chmod +x /usr/local/bin/docker-compose
    ```

    - 如果因为网络原因无法下载，可以使用以下命令获取到下载地址（在服务器上执行），接着通过能下载的机器下载该文件，并远程复制到`/usr/local/bin/docker-compose`路径：

    ```bash
    echo "https://github.com/docker/compose/releases/download/1.25.0/docker-compose-$(uname -s)-$(uname -m)"
    ```

    - 验证安装

    ```bash
    docker-compose --version
    # docker-compose version 1.25.0, build 1110ad01
    ```

    - 如果提示未找到文件，请参阅[此处](./cannot-find-docker-compose.md)

11. 配置非root用户运行

    - 参阅[FAQ](./faq.md#配置非root用户运行)
