#! -*- coding: utf-8 -*-
from datetime import datetime
from app import db, flask_bcrypt
from sqlalchemy.ext.hybrid import hybrid_property

author_abstracts = db.Table('author_abstracts',
        db.Column('author_id', db.Integer,
            db.ForeignKey('scopus_authors.id')),
        db.Column('abstract_id', db.Integer,
            db.ForeignKey('scopus_abstracts.id')))

# area_abstracts = db.Table('area_abstracts',
#         db.Column('area_id', db.Integer,
#             db.ForeignKey('scopus_areas.id')),
#         db.Column('abstract_id', db.Integer,
#             db.ForeignKey('scopus_abstracts.id')))

class ScopusAffiliation(db.Model):
    __tablename__ = 'scopus_affiliations'
    id = db.Column(db.Integer(), primary_key=True)
    affil_id = db.Column(db.String(64))
    url = db.Column(db.Text())
    name = db.Column(db.String(255))
    city = db.Column(db.String(255))
    country = db.Column(db.String(255))

    def __repr__(self):
        return "<ScopusAffiliation id=%s>" % self.affil_id


class ScopusAuthor(db.Model):
    __tablename__ = 'scopus_authors'
    id = db.Column(db.Integer(), primary_key=True)
    affil_id = db.Column(db.Integer(),
                db.ForeignKey('scopus_affiliations.id'))
    abstract_id = db.Column(db.Integer(),
                db.ForeignKey('scopus_abstracts.id'))

    initials = db.Column(db.String(8))
    indexed_name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    given_name = db.Column(db.String(255))
    preferred_name = db.Column(db.String(255))
    url = db.Column(db.Text())
    auth_id = db.Column(db.String(64))

    affiliation = db.relationship('ScopusAffiliation',
                    backref=db.backref('authors', lazy='dynamic'))

    abstracts = db.relationship('ScopusAbstract',
                    secondary=author_abstracts,
                    backref=db.backref('authors', lazy='dynamic'))

    def __repr__(self):
        return "<ScopusAuthor name=%s>" % \
                (self.indexed_name.encode('utf8'))


class ScopusAbstract(db.Model):
    __tablename__ = 'scopus_abstracts'
    id = db.Column(db.Integer(), primary_key=True)
    # area_id = db.Column(db.Integer(), db.ForeignKey('scopus_areas.id'))
    url = db.Column(db.Text())
    identifier = db.Column(db.String(64))
    pii = db.Column(db.String(64))
    doi = db.Column(db.String(64))
    eid = db.Column(db.String(64))
    title = db.Column(db.Text())
    publication_name = db.Column(db.String(255))
    citedby_count = db.Column(db.Integer())
    cover_date = db.Column(db.DateTime())
    description = db.Column(db.Text())


    def __repr__(self):
        return "<ScopusAbstract title=%s, doi=%s>" % \
                                (self.title[:20], self.doi)


# class ScopusArea(db.Model):
#     __tablename__ = 'scopus_areas'
#     id = db.Column(db.Integer(), primary_key=True)
#     abstract_id = db.Column(db.Integer(),
#                     db.ForeignKey('scopus_abstracts.id'))
#     area = db.Column(db.String(255))
#     abstracts = db.relationship('ScopusAbstract',
#                         secondary=area_abstracts,
#                         backref=db.backref('areas', lazy='dynamic'))
# 
#     def __repr__(self):
#         return "<ScopusArea area=%s>" % (self.area)


class FundingAgency(db.Model):
    __tablename__ = 'funding_agencies'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Text())
    year = db.Column(db.String(12))
    amount = db.Column(db.Float())
