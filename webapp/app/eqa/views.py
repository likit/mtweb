from flask import Blueprint

eqa = Blueprint('eqa', __name__, template_folder='templates')

@eqa.route('/', methods=['GET'])
def index():
    return "You are at the eqa index page."
