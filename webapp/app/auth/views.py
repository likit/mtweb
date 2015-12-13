from flask import Blueprint

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return "Login page."

@auth.route('/register', methods=['GET', 'POST'])
def register():
    return "Register page."

@auth.route('/logout')
def logout():
    return "You have logged out."
