## ~~ 论坛用作参考（已废弃）~~

## Requirements
* python 3.6+
* pip 18.0.0+

## Installation
> 数据库不带密码只接收本地连接
* mongodb 3.*(2018.6)
* redis

```sh
pip install pymongo redis requests
pip install flask
```

## 收获
* 服务器ssh key无密码
* ln 软连接本地配置文件
* 数据库连接的登录
* log日志文件代替输出
* 密码md5 -> 加盐md5
* 上传
* 对部分请求加token验证
* 同一个逻辑名，可以映射为GET/POST/PUT/DELETE
* nginx 可以通过配置让外部端口，如80转发到本地任意端口
