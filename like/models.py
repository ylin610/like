# coding: utf-8
from like.exts import db, whooshee
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from like.utils import get_max
import hashlib
from flask import current_app


PERMISSIONS = [
    'PUBLISH',  # 发布动态
    'FOLLOW',  # 关注用户、主题
    'COLLECT',  # 收藏动态、点赞动态或评论
    'COMMENT',  # 发表评论
    'DISCUSSION',  # 参与讨论
    'ADMIN'  # 管理员
]

PERMISSION_MAP = {
    'UNVERIFIED': ['FOLLOW', 'COLLECT'],
    'USER': ['FOLLOW', 'COLLECT', 'PUBLISH', 'COMMENT', 'DISCUSSION'],
    'ADMIN': ['FOLLOW', 'COLLECT', 'PUBLISH', 'COMMENT', 'DISCUSSION', 'ADMIN']
}

role_permission = db.Table(
    'role_permission',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'), primary_key=True)
)

user_topic = db.Table(
    'user_topic',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('topic_id', db.Integer, db.ForeignKey('topic.id'), primary_key=True)
)

user_post_collect = db.Table(
    'user_post_collect',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)

user_post_like = db.Table(
    'user_post_like',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)

user_discussion = db.Table(
    'user_discussion',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('discussion_id', db.Integer, db.ForeignKey('discussion.id'), primary_key=True)
)

user_comment_like = db.Table(
    'user_comment_like',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('comment_id', db.Integer, db.ForeignKey('comment.id'), primary_key=True)
)

follow = db.Table(
    'follow',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32))

    roles = db.relationship('Role',
                            secondary=role_permission,
                            back_populates='permissions')

    @staticmethod
    def init_permission():
        for permission in PERMISSIONS:
            perm = Permission(name=permission)
            db.session.add(perm)
        db.session.commit()


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32))

    users = db.relationship('User', back_populates='role')
    permissions = db.relationship('Permission',
                                  secondary=role_permission,
                                  back_populates='roles')

    @staticmethod
    def init_role():
        for name, permission_list in PERMISSION_MAP.items():
            role = Role(name=name)
            db.session.add(role)
            for permission in permission_list:
                perm = Permission.query.filter_by(name=permission).first()
                role.permissions.append(perm)
        db.session.commit()

    # def add_permission(self, permission):
    #     perm = Permission.query.filter_by(name=permission).first()
    #     if perm in self.permissions:
    #         raise ValueError(f'角色<{self.name}>已有权限<{permission}>，请勿重复添加！')
    #     if perm is None:
    #         db.session.add(perm)


@whooshee.register_model('username', 'bio')
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    password_ = db.Column(db.String(128))
    email = db.Column(db.String(32), nullable=False, unique=True)
    email_hash = db.Column(db.String(32))
    bio = db.Column(db.String(256))
    create_time = db.Column(db.DateTime, default=datetime.now)
    # is_banned = db.Column(db.Boolean, default=False)

    role_id = db.Column(db.ForeignKey('role.id'))

    role = db.relationship('Role', back_populates='users')
    created_topics = db.relationship('Topic', back_populates='creator')
    followed_topics = db.relationship('Topic',
                                      secondary=user_topic,
                                      back_populates='followers')
    posts = db.relationship('Post', back_populates='creator', cascade='all')
    collected_posts = db.relationship('Post',
                                      secondary=user_post_collect,
                                      back_populates='collected_users')
    liked_posts = db.relationship('Post',
                                  secondary=user_post_like,
                                  back_populates='liked_users')
    comments = db.relationship('Comment', back_populates='creator', cascade='all')
    liked_comments = db.relationship('Comment',
                                     secondary=user_comment_like,
                                     back_populates='liked_users')
    created_discussions = db.relationship('Discussion', back_populates='creator')
    discussions = db.relationship('Discussion', secondary=user_discussion, back_populates='participants')
    statements = db.relationship('Statement', back_populates='creator', cascade='all')
    followed = db.relationship('User',
                               secondary=follow,
                               primaryjoin=(follow.c.follower_id == id),
                               secondaryjoin=(follow.c.followed_id == id),
                               backref=db.backref('followers')
                               )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._gen_avatar()

    def _gen_avatar(self):
        m = hashlib.md5()
        m.update(bytes(self.email, 'utf-8'))
        self.email_hash = m.hexdigest()

    @property
    def password(self):
        raise AttributeError

    @password.setter
    def password(self, password):
        self.password_ = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_, password)

    def set_role(self, role_name):
        role = Role.query.filter_by(name=role_name).first()
        if role is None:
            raise ValueError(f'角色<{role}>不存在！')
        elif role is self.role:
            raise ValueError(f'用户<{self.username}>已是角色<{role_name}>，请勿重复设置！')
        else:
            self.role = role

    def has_permission(self, *args):
        for permission in args:
            perm = Permission.query.filter_by(name=permission).first()
            if perm is None:
                raise LookupError(f'权限<{perm}>不存在！')
            elif perm not in self.role.permissions:
                return False
        return True

    def is_verified(self):
        unverified = Role.query.filter_by(name='UNVERIFIED')
        return self.role is not unverified

    def avatar(self, size=None):
        if not size:
            size = current_app.config.get('AVATAR_SIZE', 40)
        return f'https://www.gravatar.com/avatar/{self.email_hash}?d=identicon&s={size}'


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), nullable=False, unique=True)
    description = db.Column(db.String(256))
    create_time = db.Column(db.DateTime, default=datetime.now, index=True)

    creator_id = db.Column(db.ForeignKey('user.id'))

    creator = db.relationship('User', back_populates='created_topics')
    followers = db.relationship('User',
                                secondary=user_topic,
                                back_populates='followed_topics')
    posts = db.relationship('Post', back_populates='topic')

    def get_hot_posts(self, num=5):
        return get_max(self.posts, num=num, key=lambda x: len(x.liked_users))


@whooshee.register_model('content')
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(512), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now, index=True)

    creator_id = db.Column(db.ForeignKey('user.id'))
    topic_id = db.Column(db.ForeignKey('topic.id'))

    topic = db.relationship('Topic', back_populates='posts')
    creator = db.relationship('User', back_populates='posts')
    collected_users = db.relationship('User',
                                      secondary=user_post_collect,
                                      back_populates='collected_posts')
    liked_users = db.relationship('User',
                                  secondary=user_post_like,
                                  back_populates='liked_posts')
    comments = db.relationship('Comment', back_populates='post', cascade='all')

    def get_hot_comments(self, num=1):
        return get_max(self.comments, num=num, key=lambda x: len(x.liked_users))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(512), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now, index=True)

    creator_id = db.Column(db.ForeignKey('user.id'))
    post_id = db.Column(db.ForeignKey('post.id'))
    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))

    creator = db.relationship('User', back_populates='comments')
    post = db.relationship('Post', back_populates='comments')
    liked_users = db.relationship('User',
                                  secondary=user_comment_like,
                                  back_populates='liked_comments')

    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])
    replies = db.relationship('Comment', back_populates='replied', cascade='all')

    @property
    def ordered_replies(self):
        return sorted(self.replies, key=lambda x: x.create_time, reverse=True)


class Discussion(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    start_time = db.Column(db.DateTime)

    creator_id = db.Column(db.ForeignKey('user.id'))

    creator = db.relationship('User', back_populates='created_discussions')
    participants = db.relationship('User',
                                   secondary=user_discussion,
                                   back_populates='discussions')
    statements = db.relationship('Statement', back_populates='discussion', cascade='all')


class Statement(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(512), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now, index=True)

    creator_id = db.Column(db.ForeignKey('user.id'))
    discussion_id = db.Column(db.ForeignKey('discussion.id'))

    creator = db.relationship('User', back_populates='statements')
    discussion = db.relationship('Discussion', back_populates='statements')
