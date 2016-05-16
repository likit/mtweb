import requests
import xml.etree.ElementTree as et
import json
import time
import re
from datetime import datetime
from collections import namedtuple, defaultdict
from operator import itemgetter

from flask import (Blueprint, render_template, request,
                    flash, redirect, url_for, abort)
from flask.ext.login import login_required, current_user
from app import db
from app.research.models import ScopusAbstract, ScopusAuthor, FundingAgency
from app import backoffice

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


@research.route('/overview/')
def overview():
    author_count = defaultdict(int)
    ppy = defaultdict(int) # pub per year
    cpy = defaultdict(int) # citation per year
    h_index = defaultdict(list)
    total_articles = 0
    for p in ScopusAbstract.query.all():
        total_articles += 1
        for a in p.authors:
            key = a.given_name + '|' + a.surname
            author_count[key] += 1

        ppy[p.cover_date.year] += 1
        cpy[p.cover_date.year] += int(p.citedby_count)
        h_index[p.cover_date.year].append(int(p.citedby_count))

    year_range = range(min(sorted(ppy.keys())),
                        datetime.utcnow().year+1)
    for k in h_index:
        h_index[k] = sorted(h_index[k], reverse=True)

    h_index_per_year = []
    for i in year_range:
        if i in h_index:
            for n, k in enumerate(h_index[i], start=1):
                if n > k:
                    h_index_per_year.append({'key': i, 'y': n-1})
                    break
        else:
            h_index_per_year.append({'key': i, 'y': 0})

    print(h_index_per_year)

    pub_per_year = []
    for i in year_range:
        if i in ppy:
            pub_per_year.append({'key': i, 'y': ppy[i]})
        else:
            pub_per_year.append({'key': i, 'y': 0})

    cite_per_year = []
    for i in year_range:
        if i in cpy:
            cite_per_year.append({'key': i, 'y': cpy[i]})
        else:
            cite_per_year.append({'key': i, 'y': 0})

    cite_per_year_data=[{'values': cite_per_year,
                            'key': 'Citation',
                            'color': '#F90321'}
                            ]

    all_per_year_data=[{'values': [[c['key'], c['y']] for c in cite_per_year],
                            'key': 'Citation',
                            'color': '#333'},
                        {'values': [[p['key'], p['y']] for p in pub_per_year],
                            'key': 'Publication',
                            'bar': True,
                            'color': '#ccf'}
                            ]

    h_pub_per_year_data=[{'values': [[c['key'], c['y']] for c in h_index_per_year],
                            'key': 'h-index',
                            'color': '#333'},
                        {'values': [[p['key'], p['y']] for p in pub_per_year],
                            'key': 'Publication',
                            'bar': True,
                            'color': '#ccf'}
                            ]

    pub_per_year_data=[{'values': pub_per_year,
                            'key': 'Publication',
                            'color': '#0033cc'}
                            ]
    import operator

    top_author_count = sorted(author_count.items(),
                            key=operator.itemgetter(1))[:10]

    data = []
    cumcitation = 0
    for i in year_range:
        cumcitation += cpy.get(i, 0)
        data.append((i, ppy.get(i, 0), cpy.get(i, 0), cumcitation))

    # h_index = sorted(h_index, key=itemgetter(1), reverse=True)
    # print(h_index[:10])

    return render_template('research/overview.html',
            pub_per_year=pub_per_year_data,
            cite_per_year=cite_per_year_data,
            all_per_year=all_per_year_data,
            h_pub_per_year=h_pub_per_year_data,
            top_author_count=top_author_count,
            data=data,
            total_articles=total_articles,
            cumcitation=cumcitation,
            )


@research.route('/overview/<int:year>')
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

    pub_per_month_data=[{'values': pub_per_month, 'key': 'Publication'}]

    fundings = [{"label": f.name, "value": f.amount}
                for f in FundingAgency.query.filter_by(year=str(year))]
    tyf = sum([i['value'] for i in fundings])

    import locale
    pub_cost = tyf/len(pubs)
    locale.setlocale(locale.LC_ALL, 'en_US.utf-8')
    tyf = locale.currency(tyf, symbol=False, grouping=True)
    pub_cost = locale.currency(pub_cost, symbol=False, grouping=True)


    return render_template('research/index.html',
            pubs=abstracts,
            year=year,
            pub_per_month=pub_per_month_data,
            total_year_funding=tyf,
            fundings=fundings,
            pub_cost=pub_cost)


@research.route('/research/profile/')
def profile():
    firstname = request.args.get('firstname')
    lastname = request.args.get('lastname')
    # lastname = 'Worachartcheewan'
    # firstname = 'Apilak'
    author = ScopusAuthor.query.filter_by(given_name=firstname,
                                            surname=lastname).first()
    abstracts = []
    if author:
        ppy = defaultdict(int)
        for p in author.abstracts:
            authors = ', '.join([a.indexed_name for a in p.authors])
            year = p.cover_date.year
            ppy[year] += 1
            abstracts.append(Abstract(
                                doi=p.doi,
                                title=p.title,
                                authors=authors,
                                year=year,
                                url=p.url,
                                citedby_count=p.citedby_count,
                                publication_name=p.publication_name,
                            ))

        pub_per_year = []
        year_range = range(min(sorted(ppy.keys())),
                            datetime.utcnow().year+1)
        for i in year_range:
            if i in ppy:
                pub_per_year.append({'key': i, 'y': ppy[i]})
            else:
                pub_per_year.append({'key': i, 'y': 0})

        pub_per_year_data=[{'values': pub_per_year, 'key': 'Publication'}]

        return render_template('research/profile.html',
                                    pubs=abstracts, author=author,
                                    pub_per_year=pub_per_year_data)
    else:
        return 'Hi,'
