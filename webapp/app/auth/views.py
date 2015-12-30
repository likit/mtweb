from flask import (Blueprint, render_template, redirect, url_for, flash)
from app import flask_bcrypt, db
from .forms import LoginForm, RegisterForm
from app.models import User, Role, UserType
from flask.ext.login import login_user, logout_user

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and flask_bcrypt.check_password_hash(user.password,
                form.password.data):
            login_user(user)
            flash('Welcome %s %s. You have logged in successfully.'
                    % (user.firstname, user.lastname))
            return redirect(url_for('main.index'))
        else:
            flash('User not found.')
    form.email.data = ''
    form.password.data = ''
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email has already been used.')
            return render_template('auth/register.html', form=form)
        else:
            role = Role.query.filter_by(default=True).first()
            if (form.email.data.endswith('mahidol.edu') or
                    form.email.data.endswith('mahidol.ac.th')):
                # check the student database
                # check the staff database
                user_type = UserType.STUDENT
            else:
                user_type = UserType.CUSTOMER

            user = User(firstname=form.firstname.data,
                    lastname=form.lastname.data,
                    email=form.email.data,
                    password=form.password.data,
                    role=role, user_type=user_type)

            db.session.add(user)
            db.session.commit()
            flash('Registered successfully.')
            return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
