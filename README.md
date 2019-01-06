# 立刻 - Like

## 简介

立刻（Like）是一个类似[即刻](https://www.ruguoapp.com/)的兴趣交流平台，支持创建话题、在话题下发表动态、创建讨论组实时聊天，以及相关的收藏、点赞、评论、回复等操作。

## 如何使用

- 访问 [http:like.stravel.top](http://like.stravel.top)，使用测试帐号（admin@test.com:1234）登录即可；
- 克隆源码本地运行。

## 技术栈

- Flask
    该项目基于的 Python Web 框架。
- MySql
    存放常规数据。
- MongoDB
    存放用户的通知消息。
- Memcached
    存放验证码。
- Celery
    异步发送邮件。
- Redis
    Celery 的 Broker 和 Backend。
- Nginx
    Web 服务器。
- Gunicorn
    WSGI 服务器。
- Supervisor
    管理 Gunicorn 进程。
