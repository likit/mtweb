from flask import Blueprint, render_template, redirect, url_for

relations = Blueprint('relations', __name__, template_folder='templates')

@relations.route('/')
def index():
    return render_template('relations/index.html')
