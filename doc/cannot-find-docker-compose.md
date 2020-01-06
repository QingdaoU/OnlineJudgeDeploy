# Cannot find /usr/bin/docker-compose 的解决办法

1. 确认已经安装`docker-compose`

1. 执行`whereis docker-compose`找到`docker-compose`的安装位置，例如pip会将其安装在`/usr/local/bin/docker-compose`

1. 建立软链接

```bash
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```

- 如果安装路径不在/usr/local/bin，将第一个路径换成实际的安装位置

4. 验证

```bash
docker-compose version
# docker-compose version 1.25.0, build 1110ad01
```