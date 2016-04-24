# -*- coding: utf8 -*-
from flask import (Blueprint, render_template,
                    flash, redirect, url_for, request, abort)
from app.models import (SystemPermission, User, Department,
                        UserType, AcademicPosition, ForumPermission,
                        Title, Job, RoomDirectory)
from flask.ext.login import login_required, current_user
from .forms import EditProfileForm, AdminEditProfileForm
from app import db
from operator import itemgetter

main = Blueprint('main', __name__, template_folder='templates')


def flash_errors(form):
    '''
    Show errors from wtforms using flash.

    '''
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error))


@main.route('/', methods=['GET'])
def index():
    return render_template('main/index.html')


# make permission available in all templates
@main.app_context_processor
def inject_permission():
    return dict(SystemPermission=SystemPermission,
                ForumPermission=ForumPermission)

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
    acad_positions = [(d.id, d.en_title)
            for d in AcademicPosition.query.order_by('level').all()]
    form.academic_position.choices = sorted(acad_positions, key=lambda x: x[0])
    departments = [(d.en_name, d.en_name) for d in Department.query.all()]
    form.department.choices = sorted(departments, key=itemgetter(1))

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.faculty_info.car_license_plate = \
                                form.car_license_plate.data
        current_user.academic_position = form.academic_position.data
        current_user.contact.mobile_phone = form.mobile_phone.data
        current_user.contact.fax = form.fax.data

        db.session.add(current_user)
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', email=current_user.email))
    else:
        flash_errors(form)

    form.username.data = current_user.username
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    if current_user.faculty_info:
        form.mobile_phone.data = current_user.contact.mobile_phone
        form.fax.data = current_user.contact.fax
        form.car_license_plate.data = \
                current_user.faculty_info.car_license_plate
        form.faculty_info.academic_position.default = \
                current_user.faculty_info.academic_position.id
    return render_template('main/edit_profile.html', form=form)


@main.route('/department/<int:did>')
@main.route('/department/')
def department(did=None):
    '''
    did = Department ID
    '''
    if did:
        department = Department.query.get(did)
        if department:
            return render_template('main/department.html',
                    department=department)
        else:
            return "Department ID not found."
    else:
        abort(404)


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('main/404.html'), 404


@main.route('/edit_profile_by_admin/<email>',
                        methods=['GET', 'POST'])
@main.route('/edit_profile_by_admin/',
                        methods=['GET', 'POST'])
def edit_profile_by_admin(email=None):
    '''
    For an admin to edit user's profile.
    '''
    form = AdminEditProfileForm()
    # Setup dynamic select fields from data tables.
    # Choices have to be set before validate_on_submit is invoked.
    titles = [(t.id, '%s / %s' %(t.th_name, t.en_name))
                for t in Title.query.all()]
    acad_positions = [(d.id, '%s / %s' % (d.th_title, d.en_title))
            for d in AcademicPosition.query.order_by('level').all()]
    departments = [(d.id, '%s / %s' % (d.th_name, d.en_name))
                for d in Department.query.order_by('th_name').all()]
    jobs = [(j.id, '%s / %s' % (j.th_name, j.en_name))
                    for j in Job.query.order_by('th_name').all()]
    office = [(o.id, o.roomid)
            for o in RoomDirectory.query.order_by('roomid').all()]

    # Select field
    form.job.choices = jobs
    form.academic_position.choices = acad_positions
    form.department.choices = departments
    form.title.choices = titles
    form.office.choices = office


    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).one()
        if not user:
            flash('{} has not been registered in the system.'.format(email))
            return redirect(url_for('.index'))
        else:
            user.username = form.username.data
            user.email = form.email.data
            user.th_firstname = form.th_firstname.data
            user.th_lastname = form.th_lastname.data
            user.en_firstname = form.en_firstname.data
            user.en_lastname = form.en_lastname.data
            user.about_me = form.about_me.data
            user.title = Title.query.get(form.title.data)
            user.department = Department.query.get(form.department.data)
            user.job = Job.query.get(form.job.data)

            academic_position = \
                    AcademicPosition.query.get(form.academic_position.data)
            if not user.faculty_info:
                user.faculty_info = FacultyInfo(
                        car_license_plate=form.car_license_plate.data,
                        department_head=False,
                        academic_position=academic_position,
                        )
            else:
                user.faculty_info.car_license_plate = \
                        form.car_license_plate.data
                user.faculty_info.department_head = False
                user.faculty_info.academic_position = academic_position

            office = RoomDirectory.query.get(form.office.data)
            if not user.contact:
                user.contact = Contact(
                        office=office,
                        mobile_phone=form.mobile_phone.data,
                        fax=form.fax.data,
                        )
            else:
                user.contact.office = office
                user.contact.mobile_phone = form.mobile_phone.data
                user.contact.fax = form.fax.data

            flash('Data has been saved.')
            return redirect(url_for('.edit_profile_by_admin',
                                            email=form.email.data))
    else:
        flash_errors(form)
        if not email:
            abort(404)

        user = User.query.filter_by(email=email).one()
        if not user:
            flash('{} has not been registered in the system.'.format(email))
        else:
            # Populate some fields with previously entered data, if any.
            if user.faculty_info.academic_position:
                form.academic_position.default = \
                        user.faculty_info.academic_position.id
            form.department.default = user.department.id
            form.title.default = user.title.id or ''
            form.job.default = user.job.id or ''
            form.office.default = user.contact.office.id
            form.process()

            # Other fields
            form.email.data = user.email
            form.gender.data = user.gender
            form.th_firstname.data = user.th_firstname
            form.th_lastname.data = user.th_lastname
            form.en_firstname.data = user.en_firstname
            form.en_lastname.data = user.en_lastname
            form.username.data = user.username
            form.about_me.data = user.about_me
            form.mobile_phone.data = user.contact.mobile_phone
            form.fax.data = user.contact.fax

            # If faculty info has been created.
            if user.faculty_info:
                form.car_license_plate.data = \
                        user.faculty_info.car_license_plate

            return render_template('main/edit_profile_admin.html',
                                                user=user, form=form)
