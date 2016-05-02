import requests
import xml.etree.ElementTree as et
import json
import time
import re
from datetime import datetime
from collections import namedtuple, defaultdict

from flask import (Blueprint, render_template,
                    flash, redirect, url_for, abort)
from flask.ext.login import login_required, current_user
from app import db
from app.research.models import ScopusAbstract, ScopusAuthor

research = Blueprint('research', __name__, template_folder='templates')

api_key = '871232b0f825c9b5f38f8833dc0d8691'

Abstract = namedtuple('Abstract',
        ['url', 'doi', 'title', 'citedby_count',
            'year', 'authors', 'publication_name'])

url = 'http://api.elsevier.com/content/search/scopus'

def flash_errors(form):
    '''
    Show errors from wtforms using flash.

    '''
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error))


@research.route('/overview/<int:year>')
@research.route('/overview/')
def index(year=None):

    # just a hack to get pubs in a certain year
    # we will refactor this later, probably using hybrid attribute.
    pubs = [pub for pub in ScopusAbstract.query.all()
                if pub.cover_date.year == year]
    abstracts = []
    ppm = defaultdict(int)
    for p in pubs:
        authors = ', '.join([a.indexed_name for a in p.authors])
        year = p.cover_date.year
        ppm[p.cover_date.month] += 1
        abstracts.append(Abstract(
                            doi=p.doi,
                            title=p.title,
                            authors=authors,
                            year=year,
                            url=p.url,
                            citedby_count=p.citedby_count,
                            publication_name=p.publication_name,
                        ))

    pub_per_month = []
    for i in range(1,13):
        if i in ppm:
            pub_per_month.append({'key': i, 'y': ppm[i]})
        else:
            pub_per_month.append({'key': i, 'y': 0})

    print(pub_per_month)

    pub_per_month_data=[{'values': pub_per_month, 'key': 'Month'}]

    return render_template('research/index.html',
            pubs=abstracts, year=year, pub_per_month=pub_per_month_data)
