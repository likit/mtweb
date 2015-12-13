from flask import Blueprint, render_template

services = Blueprint('services', __name__,
                                template_folder='templates')

@services.route('/', methods=['GET'])
def index():
    return render_template('services/index.html')
