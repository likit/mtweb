# -*- coding: utf8 -*-
from __future__ import print_function
import json
import httplib2

import gspread
from collections import defaultdict
from flask import (Blueprint, render_template, request,
                    flash, redirect, url_for, request, abort, session)
from flask.ext.login import login_required, current_user
from app import db
from operator import itemgetter
from app.decorators import webadmin_required
from apiclient import discovery
from oauth2client import client
from app.research.models import FundingAgency
from app.academics.models import (QStakeholderTakers, QStakeholders,
                                    QStakeholderQuestion,
                                    QWellrounded, QWellroundedTaker,
                                    QWellroundedQuestion)

backoffice = Blueprint('backoffice', __name__, template_folder='templates')


def flash_errors(form):
    '''
    Show errors from wtforms using flash.

    '''
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error))

# File list
# https://developers.google.com/drive/v3/reference/files/list#request

# Search for files
# https://developers.google.com/drive/v3/web/search-parameters#examples

# File references
# https://developers.google.com/drive/v3/reference/files/get#http-request

# Supported MIME type
# https://developers.google.com/drive/v3/web/mime-types

@backoffice.route('/gdrive/authorize')
def index():
    if 'credentials' not in session:
        return redirect(url_for('backoffice.oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    if credentials.access_token_expired:
        return redirect(url_for('backoffice.oauth2callback'))
    else:
        http_auth = credentials.authorize(httplib2.Http())
        drive_service = discovery.build('drive', 'v3', http_auth)
        return render_template('backoffice/index.html')


@backoffice.route('/gdrive/oauth2callback')
def oauth2callback():
    flow = client.flow_from_clientsecrets(
            'client_secrets.json',
            scope = 'https://www.googleapis.com/auth/drive.metadata.readonly https://spreadsheets.google.com/feeds',
            redirect_uri=url_for('backoffice.oauth2callback', _external=True),
            )
    if 'code' not in request.args:
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
    else:
        auth_code = request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        session['credentials'] = credentials.to_json()
        return redirect(url_for('backoffice.index'))


@backoffice.route('/gdrive/loadsheet/<id>')
def loadsheet(id):
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    gc = gspread.authorize(credentials)
    worksheet = gc.open_by_key(id).sheet1
    val = worksheet.acell('A2').value
    return str(val)


def parse_funding_data(worksheet, agencies, years):
    row = 4  # a starting row
    print(worksheet.title)
    while True:
        fund_cell = 'D%d' % row
        agency_cell = 'A%d' % row
        val = worksheet.acell(fund_cell).value
        if val == 'END':
            return
        elif val.strip() == '':
            agency = worksheet.acell(agency_cell).value
            row += 1
            continue
        else:
            agencies[agency][worksheet.title] = float(val)
            years[worksheet.title] += float(val)
            row += 1


@backoffice.route('/update/funding')
def update_research_funding(year=None):
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    gc = gspread.authorize(credentials)
    # worksheet = gc.open("research_funds.xls").sheet1
    workbook = gc.open("research_funds.xls")
    agencies = defaultdict(dict)
    years = defaultdict(float)

    if not year:
        for worksheet in workbook.worksheets():
            parse_funding_data(worksheet, agencies, years)
    else:
        worksheet = workbook.worksheet(year)
        parse_funding_data(worksheet, agencies, years)

    for a in agencies:
        for y in agencies[a]:
            fund = FundingAgency.query.filter_by(year=y, name=a).first()
            if fund:
                if fund.amount != agencies[a][y]:
                    fund.amount = agencies[a][y]  # update the new amount
                else:
                    continue
            else:
                fund = FundingAgency(name=a, year=y, amount=agencies[a][y])
            db.session.add(fund)
    db.session.commit()
    flash('Fundings update is finished.')
    return redirect(url_for('backoffice.index'))


@backoffice.route('/update/academics/stakeholders-eval-data')
def update_stakeholder_eval():
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    http_auth = credentials.authorize(httplib2.Http())
    drive_service = discovery.build('drive', 'v3', http_auth)
    res = drive_service.files().list(q="name contains 'graduate_eval'").execute()
    gc = gspread.authorize(credentials)
    for f in [f['name'] for f in res['files']]:
        worksheet = gc.open(f).sheet1
        discipline, year = f.split('.')[0].split('_')[-2:]
        row = 1
        headings = worksheet.row_values(row)
        question = QStakeholderQuestion.query.filter_by(qtext=headings[10]).first()
        if not question:
            print('Create question table...')
            for n, qtext in enumerate(headings):
                q = QStakeholderQuestion(qtext=qtext,
                                order=n, discipline=discipline)
                db.session.add(q)
            db.session.commit()

        while True:
            row += 1
            data = worksheet.row_values(row)
            name = data[1]
            if name == 'END':
                break
            position = data[2]
            institution_type = [3]
            affiliation = data[4]
            alumni = data[5]
            supervisor_position = data[6]
            assigned_rep_position = data[7]
            try:
                executive_year = int(data[8])
            except ValueError:
                executive_year = 0
            qyear = year
            discipline = discipline
            taker = QStakeholderTakers(name=name,
                    affiliation=affiliation,
                    position=position,
                    alumni=alumni,
                    institution_type=institution_type,
                    supervisor_position=supervisor_position,
                    assigned_rep_position=assigned_rep_position,
                    executive_year=executive_year,
                    qyear=qyear,
                    )
            for i in range(10, len(data)):
                question = QStakeholderQuestion.query.filter_by(qtext=headings[i],
                        discipline=discipline).first()
                answer = QStakeholders(qanswer=data[i], qyear=year)
                question.answers.append(answer)
                taker.questions.append(question)
        flash('Data updated.')
    return redirect(url_for('backoffice.index'))


@backoffice.route('/update/academics/wellrounded-data')
def update_wellrounded():
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    http_auth = credentials.authorize(httplib2.Http())
    drive_service = discovery.build('drive', 'v3', http_auth)
    res = drive_service.files().list(q="name contains 'wellrounded'").execute()
    gc = gspread.authorize(credentials)
    for f in [f['name'] for f in res['files']]:
        worksheet = gc.open(f).sheet1
        year = f.split('.')[0].split('-')[-1]
        row = 1
        # answer = QWellrounded.query.filter_by(qyear=year).first()
        # if answer:
        #     print('%s data have been imported to the database. Skipped.')
        #     continue
        headings = worksheet.row_values(row)
        question = QWellroundedQuestion.query.filter_by(qtext=headings[3]).first()
        if not question:  # no questions in the db yet
            print('Creating question table..')
            for n, heading in enumerate(headings):
                question = QWellroundedQuestion(order=n, qtext=heading)
                db.session.add(question)
            db.session.commit()
        import time
        while True:
            row += 1
            if row % 10 == 0:
                print('Sleeping...')
                time.sleep(5)

            discipline = worksheet.cell(row, 2).value
            if discipline == 'END':  # reached the last record.
                break

            fullname = worksheet.cell(row, 3).value
            taker = QWellroundedTaker.query.filter_by(fullname=fullname).first()

            if taker:  # this record exists.
                print('{} This record has been imported already. Skipped.'.format(fullname.encode('utf8')))
                continue

            line_id = worksheet.acell('HM%d' % row).value
            facebook_id = worksheet.acell('HN%d' % row).value
            email = worksheet.acell('HO%d' % row).value
            taker = QWellroundedTaker(discipline=discipline,
                                        fullname=fullname,
                                        line_id=line_id,
                                        facebook_id=facebook_id,
                                        email=email,
                                        )
            data = worksheet.row_values(row)
            for i in range(len(headings)):
                heading = headings[i]
                value = data[i]
                answer = QWellrounded(qanswer=value, qyear=year)
                question = QWellroundedQuestion.query.filter_by(qtext=heading).first()
                if question:
                    question.answers.append(answer)
                    taker.questions.append(answer)
                    db.session.add(taker)
                    db.session.add(question)
            db.session.commit()
            print('{} done.'.format(taker.fullname.encode('utf8')))
    flash('Data downloaded.')
    return redirect(url_for('backoffice.index'))
