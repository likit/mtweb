from flask import Blueprint, render_template

eqa = Blueprint('eqa', __name__, template_folder='templates')

@eqa.route('/', methods=['GET'])
def index():
    return render_template('eqa/index.html')
