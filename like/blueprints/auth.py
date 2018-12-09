# coding: utf-8
from flask import Blueprint, redirect, url_for, render_template
from flask_login import current_user, login_user, logout_user, login_required
from like.forms import SignUpForm, LoginForm
from like.models import User
from like.exts import db


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('front.index'))
    form = SignUpForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = User(username=username, email=email)
        user.password = password
        user.set_role('UNVERIFIED')
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('front.index'))
    else:
        print(form.errors)
        return render_template('auth/signup.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('front.index'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user is None:
            return redirect(url_for('auth.login'))
        if user.check_password(password):
            login_user(user)
            return redirect(url_for('front.index'))
        else:
            return redirect(url_for('auth.login'))
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('front.index'))
