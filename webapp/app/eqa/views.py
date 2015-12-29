from flask import Blueprint, render_template, flash, redirect, url_for
from flask.ext.login import login_required, current_user
from .forms import ResultForm
from app.models import LabInfo

eqa = Blueprint('eqa', __name__, template_folder='templates')

@eqa.route('/', methods=['GET'])
# @login_required
def index():
    if current_user.is_authenticated:
        if current_user.labinfo:
            return redirect(url_for('eqa.results'))
        else:
            flash('You need to add lab information to proceed.')
            return redirect(url_for('customers.add_lab_info'))

@eqa.route('/results', methods=['GET'])
# @login_required
def results():
    form = ResultForm()
    return render_template('eqa/results.html', form=form)
