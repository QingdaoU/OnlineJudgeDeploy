# 常见问题

## 安装依赖组件超时或速度慢

- 请检查网络连接，国内服务器请自行切换至国内apt源，比如[中科大源](http://mirrors.ustc.edu.cn/help/ubuntu.html)。

## 国内服务器安装Docker超时或速度慢

- 请参阅[Docker安装教程](./ubuntu-docker-installation.md)使用阿里云软件源安装Docker。

## Docker pull 或 docker-compose pull 超时速度慢

- 请参阅[安装说明](../README.md)步骤4 [国内服务器配置Docker镜像源]。

## 安装docker-compose后运行提示/usr/bin/docker-compose: No such file or directory

- 参阅[此处](./cannot-find-docker-compose.md)

## Couldn't connect to Docker daemon at ... - is it running?

- 请检查Docker daemon是否在运行，使用命令`sudo systemctl status docker`或者`sudo service docker status`

- 请检查是否由root用户（或sudo）执行docker或`docker-compose`

- 如需使用非root用户操作docker请参阅本条下方 [配置非root用户运行]。

## 配置非root用户运行

- 如果需要非root用户也能运行docker（例如运维不开放root用户），执行以下命令将该用户添加到docker用户组

```bash
sudo usermod -aG docker ${用户名}
```

- 配置完成后，需要**重新登录**。

- 注意：将非root添加至`docker`用户组后，由该用户运行的容器仍可获得root权限，可能会有一定安全隐患。[参阅](https://docs.docker.com/engine/security/security/#docker-daemon-attack-surface)

## 国内服务器配置阿里云Docker镜像仓库

1. 首先你需要一个阿里云账户

1. 打开产品与服务-弹性计算-容器镜像服务，或者[点这个链接](https://cr.console.aliyun.com/cn-hangzhou/instances/mirrors)

1. 点击左侧「镜像加速器」，参考「配置镜像加速器」提供的地址和代码配置阿里云Docker镜像源。

- 注意：如果使用WSL2，配置完成后会提示无法调用systemd，请使用`sudo service docker restart`重启Docker服务。