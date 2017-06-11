这是一个新的部署脚本，应该会非常方便了。之前的部署很多不科学的地方，大家可以测试下。

安装完 docker 和 docker-compose 之后，修改 docker-compose.yml 第28行为自定义的密码，比如`rpc_token=123456`。

然后 `docker-compose up -d` ，不需要其他的步骤，大约一分钟之后 web 界面就可以访问了，默认开放80和443端口。其中443端口是自签名证书。

超级管理员用户名是root，默认密码是`password@root`，请及时修改。

登录`/admin`，添加一个判题服务器，地址为judger，端口为8080，密码是上面自定义的`rpc_token`。

修改`custom_settings.py`可以自定义站点信息。
