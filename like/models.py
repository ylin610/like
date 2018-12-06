# coding: utf-8
from like.exts import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


permissions = [
    'PUBLISH',      # 发布动态
    'FOLLOW',       # 关注用户、主题
    'COLLECT',      # 收藏动态
    'COMMENT',      # 发表评论
    'DISCUSSION',   # 参与讨论
    'ADMIN'         # 管理员
]


permission_map = {
    'UNVERIFIED': ['PUBLISH', 'FOLLOW', 'COLLECT'],
    'USER': ['PUBLISH', 'FOLLOW', 'COLLECT', 'COMMENT', 'DISCUSSION'],
    'ADMIN': ['PUBLISH', 'FOLLOW', 'COLLECT', 'COMMENT', 'DISCUSSION', 'ADMIN']
}


role_permission = db.Table('role_permission',
                           db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
                           db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'))
                           )


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32))

    roles = db.relationship('Role', secondary=role_permission, back_populates='permissions')

    @staticmethod
    def init_permission():
        for permission in permissions:
            perm = Permission(name=permission)
            db.session.add(perm)
        db.session.commit()


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32))

    users = db.relationship('User', back_populates='role')
    permissions = db.relationship('Permission', secondary=role_permission, back_populates='roles')

    @staticmethod
    def init_role():
        for name, permission_list in permission_map.items():
            role = Role(name=name)
            db.session.add(role)
            for permission in permission_list:
                perm = Permission.query.filter_by(name=permission).first()
                role.permissions.append(perm)
        db.session.commit()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    password_ = db.Column(db.String(128))
    email = db.Column(db.String(32), nullable=False, unique=True)
    email_hash = db.Column(db.String(32))
    bio = db.Column(db.String(256))
    create_time = db.Column(db.DateTime, default=datetime.now)

    is_verified = db.Column(db.Boolean, default=False)
    is_banned = db.Column(db.Boolean, default=False)

    role_id = db.Column(db.ForeignKey('role.id'))

    role = db.relationship('Role', back_populates='users')

    @property
    def password(self):
        raise AttributeError

    @password.setter
    def password(self, password):
        self.password_ = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_, password)

    def has_permission(self, *args):
        for permission in args:
            perm = Permission.query.filter_by(name=permission).first()
            if perm is None:
                raise LookupError(f'权限<{perm}>不存在！')
            elif perm not in self.role.permissions:
                return False
        return True
