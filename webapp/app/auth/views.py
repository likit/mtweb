from flask import Blueprint, render_template, redirect, url_for
from app import flask_bcrypt
from .forms import LoginForm
from .models import User
from flask.ext.login import login_user, logout_user

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print('validating form')
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).one()
        if user and flask_bcrypt.check_password_hash(user.password,
                form.password.data):
            login_user(user)
            return redirect(url_for('eqa.index'))
        else:
            return 'User not found.'
    print('failed.')
    form.email.data = ''
    form.password.data = ''
    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    return "Register page."

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('eqa.index'))
