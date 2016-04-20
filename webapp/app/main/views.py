from flask import Blueprint, render_template, flash, redirect, url_for
from app.models import (Permission, User, Department,
                            UserType, AcademicPosition)
from flask.ext.login import login_required, current_user
from .forms import EditProfileForm
from app import db
from operator import itemgetter

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
    print('Before form validation..')
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        # if current_user.user_type in [UserType.TEACHER, UserType.STAFF]:
        #     current_user.department = Department.query.filter_by(en_name=form.department.data).first()
        #     current_user.office_phone = form.office_phone.data
        #     current_user.office_room = form.office_room.data
        #     current_user.car_license_plate = form.car_license_plate.data
        #     current_academic_position = form.academic_position.data
        #     current_user.mobile_phone = form.mobile_phone.data
        db.session.add(current_user)
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', email=current_user.email))

    form.username.data = current_user.username
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    acad_positions = [(d.id, d.en_title) for d in AcademicPosition.query.all()]
    form.academic_position.choices = sorted(acad_positions, key=lambda x: x[0])
    departments = [(d.en_name, d.en_name) for d in Department.query.all()]
    form.department.choices = sorted(departments, key=itemgetter(1))
    return render_template('main/edit_profile.html', form=form)
