from flask import Blueprint, render_template
from app.models import Permission, User

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
