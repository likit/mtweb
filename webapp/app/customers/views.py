from flask import Blueprint, render_template, url_for, redirect
from flask.ext.login import login_required, current_user
from .forms import LabInfoForm
# from app.models import LabInfo

customers = Blueprint('customers', __name__, template_folder='templates')

@customers.route('/labinfo', methods=['GET', 'POST'])
def add_lab_info():
    form = LabInfoForm()
    labinfo = LabInfo.query.filter_by(user_id=current_user.id).first()
    if labinfo:
        return redirect(url_for('eqa.results'))

    return render_template('customers/labinfo.html', form=form)
