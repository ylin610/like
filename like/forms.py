# coding: utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, Length, Regexp, DataRequired, EqualTo


class SignUpForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired('请输入用户名')])
    email = StringField('邮箱', validators=[Email('请输入正确格式的邮箱'),
                                          DataRequired('请输入邮箱')])
    password = PasswordField('密码', validators=[DataRequired('密码不能为空')])
    password_repeat = PasswordField('重复密码', validators=[EqualTo('password', '密码输入不一致')])
    captcha = StringField('验证码', validators=[DataRequired('请输入验证码'),
                                             Regexp(r'^\d{6}$', message='验证码格式不正确')])
    submit = SubmitField('提交')
