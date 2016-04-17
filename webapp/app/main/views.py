from flask import Blueprint, render_template, flash, redirect, url_for
from app.models import Permission, User
from flask.ext.login import login_required, current_user
from .forms import EditProfileForm
from app import db

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/', methods=['GET'])
def index():
    return render_template('main/index.html')


# make permission available in all templates
@main.app_context_processor
def inject_permission():
    return dict(Permission=Permission)

@main.route('/user/<email>')
def user(email):
    user = User.query.filter_by(email=email).first()
    if user is None:
        abort(404)
    return render_template('main/user.html', user=user)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', email=current_user.email))
    form.username.data = current_user.username
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('main/edit_profile.html', form=form)
