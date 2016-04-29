from functools import wraps
from flask import abort
from flask.ext.login import current_user
from app.models import ForumPermission, UserType


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(ForumPermission.ADMINISTER)(f)


def correct_user_type_required(utype):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.correct_user_type(utype):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def student_required(f):
    return correct_user_type_required('STUDENT')(f)


def faculty_required(f):
    return correct_user_type_required('FACULTY')(f)


def staff_required(f):
    return correct_user_type_required('STAFF')(f)


def customer_required(f):
    return correct_user_type_required('CUSTOMER')(f)


def webadmin_required(f):
    return correct_user_type_required('ADMINISTRATOR')(f)
