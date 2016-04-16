from flask import Blueprint, render_template
from app.models import Permission

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/', methods=['GET'])
def index():
    return render_template('main/index.html')


# make permission available in all templates
@main.app_context_processor
def inject_permission():
    return dict(Permission=Permission)

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)
