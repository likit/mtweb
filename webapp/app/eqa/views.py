from flask import Blueprint, render_template
from flask.ext.login import login_required
from .forms import ResultForm

eqa = Blueprint('eqa', __name__, template_folder='templates')

@eqa.route('/', methods=['GET'])
def index():
    return render_template('eqa/index.html')

@eqa.route('/customer/results', methods=['GET'])
@login_required
def customer_results():
    form = ResultForm()
    return render_template('eqa/results.html', form=form)
