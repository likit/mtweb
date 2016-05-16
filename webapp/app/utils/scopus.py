''' Retrieve publications from Scopus APIs and add them to the database.

'''

import sys
import requests
import time
import xml.etree.ElementTree as et
import re
from datetime import datetime
from app import db
from app.research.models import ScopusAbstract, ScopusAuthor
from collections import defaultdict

API_KEY = '871232b0f825c9b5f38f8833dc0d8691'

ITEM_PER_PAGE = 20
SLEEPTIME = 5

def parse_tag(element):
    return re.match('(\{([^}]+)\})(.*)',
            element.tag.encode('utf-8')).groups()[-1]


def add_abstract(coredata):
    if not coredata:
        return None

    d = {}
    for i in coredata:
        for k, v in i.iteritems():
            d[k] = v[0].text

    new_abstract = ScopusAbstract(url=d.get('url', ''),
                            title=d.get('title', ''),
                            identifier=d.get('identifier', ''),
                            pii=d.get('pii', ''),
                            doi=d.get('doi', ''),
                            eid=d.get('eid', ''),
                            publication_name=d.get('publicationName', ''),
                            citedby_count=d.get('citedby-count', ''),
                            cover_date=d.get('coverDate', ''),
                            description=d.get('description', '')
                            )
    abstract = ScopusAbstract.query.filter_by(doi=d.get('doi')).first()
    if abstract:
        print('Article already in the database.')
        return None
    else:
        print('New article.')
        db.session.add(new_abstract)
        db.session.commit()
        return new_abstract


def add_author(authors, abstract):
    if not authors:
        return None

    for a in authors[0]['author']:
        d = {}
        for item in a:
            tag = parse_tag(item)
            d[tag] = item.text

        new_author = ScopusAuthor(initials=d.get('initials', ''),
                indexed_name=d.get('indexed-name', ''),
                surname=d.get('surname', ''),
                given_name=d.get('given-name', ''),
                preferred_name=d.get('preferred-name', ''),
                url=d.get('author-url', ''))

        author = ScopusAuthor.query.filter_by(
                given_name=new_author.given_name,
                surname=new_author.surname).first()
        if not author:
            new_author.abstracts.append(abstract)
            print('new author, {}, added.'.format(
                            new_author.indexed_name.encode('utf8')))
            db.session.add(new_author)
        else:
            author.abstracts.append(abstract)
            print('new article added to {}'.format(
                            author.indexed_name.encode('utf8')))
            db.session.add(author)
    db.session.commit()


def add_affil(affils):
    '''
    argument:
        affils = a list of affiliation elements
    '''

    for element in affils:
        for k, v in element.iteritems():
            print(k, v[0].text)


def update(year):
    query = 'AFFILORG("faculty of medical technology" "mahidol university")' \
                'AND PUBYEAR IS %s' % year

    params = {'apiKey': API_KEY, 'query': query}
    apikey = {'apiKey' : API_KEY}
    url = 'http://api.elsevier.com/content/search/scopus'

    r = requests.get(url, params=params)

    total_results = int(r.json()['search-results']['opensearch:totalResults'])
    page = 0
    article_no = 0

    print('Total articles %d' % total_results)

    for start in range(0, total_results+1, ITEM_PER_PAGE):
        page += 1
        print >> sys.stderr, \
                'Waiting %d sec to download from page %d... (%d articles/page)' \
                                            % (SLEEPTIME, page, ITEM_PER_PAGE)
        time.sleep(SLEEPTIME)
        params = {'apiKey': API_KEY,
                    'query': query,
                    'start': start,
                    'count': ITEM_PER_PAGE}

        articles = requests.get(url, params=params).json()['search-results']
        for n, entry in enumerate(articles['entry'], start=1):
            article_no += 1

            print >> sys.stderr, '%d) %s..%s' \
                    % (article_no, entry['dc:title'][:80], entry['dc:creator'][:30])

            article = requests.get(entry['prism:url'],
                                    params={'apiKey': API_KEY,})
            content = et.fromstring(article.text.encode('utf-8'))
            pub_data = defaultdict(list)
            for elem in list(content):
                try:
                    elem_tag = parse_tag(elem)
                except:
                    print(elem.tag, elem.attrib, elem.text)
                    continue
                else:
                    data = defaultdict(list)
                    for e in list(elem):
                        tag = parse_tag(e)
                        data[tag].append(e)
                    pub_data[elem_tag].append(data)

            # add_affil(pub_data.get('affiliation'))
            abstract = add_abstract(pub_data.get('coredata', None))
            if abstract:
                add_author(pub_data.get('authors'), abstract)
