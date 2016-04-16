from functools import wraps
from flask import abort
from flask.ext.login import current_user
from app.models import Permission, UserType


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
    return permission_required(Permission.ADMINISTER)(f)


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
    return correct_user_type_required(UserType.STUDENT)(f)
