from flask import (Blueprint, flash, redirect, url_for, render_template)
from app.models import User, Permission
from flask.ext.login import login_required
from app.decorators import (admin_required,
                            permission_required, student_required)

webboard = Blueprint('webboard', __name__, template_folder='templates')

@webboard.route('/admin')
@login_required
@admin_required
def for_admin_only():
    return 'For admin only'


@webboard.route('/')
@student_required
def index():
    return 'Webboard index page'

@webboard.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
    return "For moerators only."
