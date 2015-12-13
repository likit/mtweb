from flask import Blueprint

services = Blueprint('services', __name__,
                                template_folder='templates')

@services.route('/', methods=['GET'])
def index():
    return "You are at the services' index page"
