# -*- coding: utf8 -*-
import json
import httplib2

import gspread
from flask import (Blueprint, render_template, request,
                    flash, redirect, url_for, request, abort, session)
from flask.ext.login import login_required, current_user
from app import db
from operator import itemgetter
from app.decorators import webadmin_required
from apiclient import discovery
from oauth2client import client

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

@backoffice.route('/gdrive/list/<dept>')
@backoffice.route('/gdrive/list/')
def index(dept=None):
    if not dept:
        dept = 'academics'

    if 'credentials' not in session:
        return redirect(url_for('backoffice.oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    if credentials.access_token_expired:
        return redirect(url_for('backoffice.oauth2callback'))
    else:
        http_auth = credentials.authorize(httplib2.Http())
        drive_service = discovery.build('drive', 'v3', http_auth)
        folders = drive_service.files().list(
                q="name = '%s' and mimeType='application/vnd.google-apps.folder'" % dept,
                ).execute()
        if folders:
            folder_id = folders['files'][0].get('id')
            files = drive_service.files().list(
                    q="'%s' in parents and mimeType='application/vnd.google-apps.spreadsheet'" % folder_id).execute()
            return render_template('backoffice/index.html',
                                        files=files, dept=dept)
        else:
            folders = []
        return render_template('backoffice/index.html', files=folders)


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
