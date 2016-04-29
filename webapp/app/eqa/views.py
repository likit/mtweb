from flask import Blueprint, render_template, flash, redirect, url_for, abort
from flask.ext.login import login_required, current_user
from .forms import ResultForm, ActivationForm
from .models import QACustomerCode, OTPCode
from app import db

eqa = Blueprint('eqa', __name__, template_folder='templates')

def flash_errors(form):
    '''
    Show errors from wtforms using flash.

    '''
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error))


@eqa.route('/', methods=['GET'])
@login_required
def index():
    return render_template('eqa/index.html')

@eqa.route('/results/<customer_code>', methods=['GET', 'POST'])
@eqa.route('/results/', methods=['GET'])
@login_required
def results(customer_code=None):
    if not customer_code:
        abort(404)
    form = ResultForm()
    return render_template('eqa/results.html',
            form=form, customer_code=customer_code)


@eqa.route('/activate/<customer_code>', methods=['GET', 'POST'])
@eqa.route('/activate/', methods=['GET'])
@login_required
def activate(customer_code=None):
    form = ActivationForm(customer_code=customer_code)
    if form.validate_on_submit():
        cc = QACustomerCode.query.filter_by(
                customer_code=form.customer_code.data).one()
        otpcode = OTPCode.query.filter_by(code=form.code.data).one()
        if (not otpcode or otpcode.customer_code != cc):
            flash('The OTP code is not correct or has already been expired.')
        else:
            if otpcode.customer_code == cc:
                cc.current_authorized_user = current_user
                db.session.add(cc)
                db.session.commit()
                flash('Your account has been authorized.')
                return redirect(url_for('eqa.index'))
    else:
        flash_errors(form)

    if customer_code:
        cc = QACustomerCode.query.filter_by(
                customer_code=customer_code).one()
    else:
        abort(404)

    return render_template('eqa/activate.html', cc=cc, form=form)
