from flask import Blueprint

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def index():
    return 'Main index page.'
