# 立刻(Like)

## 简介

立刻（Like）是一个类似[即刻](https://www.ruguoapp.com/)的兴趣交流平台，支持创建话题、在话题下发表动态、创建讨论组实时聊天，以及相关的收藏、点赞、评论、回复等操作。

## 如何使用

- 访问 [http:like.stravel.top](http://like.stravel.top)，使用测试帐号（admin@test.com:1234）登录即可；
- 克隆源码本地运行

## 技术栈

- Flask
    该项目基于的 Python Web 框架。
- MySql
    用于存放常规数据。
- MongoDB
    用于存放用户的通知消息。
- Memcached
    用于存放验证码。
- Celery
    用于异步发送邮件。
- Redis
    用于 Celery 的 Broker 和 Backend。