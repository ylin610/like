# coding: utf-8
from flask import Blueprint, redirect, url_for, render_template
from flask_login import current_user, login_user
from like.forms import SignUpForm
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
