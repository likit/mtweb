from datetime import datetime
from collections import namedtuple, defaultdict

from flask import (Blueprint, render_template, request,
                    flash, redirect, url_for, abort)
from flask.ext.login import login_required, current_user
from app import db
from app.academics.models import (QWellroundedQuestion, QWellrounded,
                                    QStakeholders, QStakeholderQuestion)

academics = Blueprint('academics', __name__, template_folder='templates')

Survey = namedtuple('Survey', ['qtext', 'answer_avg', 'num'])

@academics.route('/wellrounded/')
def wellrounded():
    years = set()
    for q in QWellrounded.query.all():
        years.add(q.qyear)
    years = sorted(years)
    data = defaultdict(list)
    for y in years:
        for question_no in range(12, 24):
            q = QWellroundedQuestion.query.filter_by(order=question_no).first()
            print(q.qtext)
            if q:
                avg = [int(ans.qanswer) for ans in q.answers if ans.qyear==y]
                num = len(avg)
                avg = sum(avg)/float(len(avg))
                data[y].append(Survey(q.qtext, avg, num))
    questions = [s.qtext for s in data[y]]
    return render_template('academics/wellrounded.html',
            years=years, questions=questions, data=data)


@academics.route('/gradeval/')
def gradeval(year=None):
    years = set()
    for q in QStakeholders.query.all():
        years.add(q.qyear)
    years = sorted(years)
    print(years)
    for y in years:
        data = defaultdict(list)
        for question_no in [58,59,60,61,62,63]:
            q = QStakeholderQuestion.query.filter_by(order=question_no).first()
            if q:
                avg = [int(ans.qanswer) for ans in q.answers]
                num = len(avg)
                avg = sum(avg)/float(len(avg))
                data[y].append(Survey(q.qtext, avg, num))
    questions = [q.qtext for q in data[y]]
    return render_template('academics/gradeval.html', years=years,
            data=data, questions=questions)
