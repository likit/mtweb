from flask import Flask, g, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager, current_user
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from config import config
# from models import Department, User, Role

db = SQLAlchemy()
flask_bcrypt = Bcrypt()
moment = Moment()
admin = Admin()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

bootstrap = Bootstrap()


class AdminAuthentication(object):
    pass
    # def is_accessible(self):
    #     return current_user.is_authenticated \
    #             and current_user.is_administrator()


class BaseModelView(AdminAuthentication, ModelView):
    pass


class UserModelView(AdminAuthentication, ModelView):
    # _user_type_choices = [(choice, label) for choice, label in [
    #     (0x01, 'Student'),
    #     (0x02, 'Staff'),
    #     (0x04, 'Teacher'),
    #     (0x08, 'Customer'),
    #     ]]
    # column_choices = {
    #         'user_type': _user_type_choices
    #         }
    column_list = ['username', 'role_id',
                    'user_type', 'created_on',
                    'en_firstname', 'en_lastname',
                    'email', 'academic_position']
    column_searchable_list = ['en_firstname', 'en_lastname',
                                'email', 'user_type']

    # column_select_related_list = ['email']


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from research.views import research as research_blueprint
    app.register_blueprint(research_blueprint, url_prefix='/research')

    from services.views import services as services_blueprint
    app.register_blueprint(services_blueprint, url_prefix='/services')

    from eqa.views import eqa as eqa_blueprint
    app.register_blueprint(eqa_blueprint, url_prefix='/eqa')

    from auth.views import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from main.views import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='')

    from customers.views import customers as customers_blueprint
    app.register_blueprint(customers_blueprint, url_prefix='/customers')

    from relations.views import relations as relations_blueprint
    app.register_blueprint(relations_blueprint, url_prefix='/relations')

    from webboard.views import webboard as webboard_blueprint
    app.register_blueprint(webboard_blueprint, url_prefix='/webboard')

    from academics.views import academics as academics_blueprint
    app.register_blueprint(academics_blueprint, url_prefix='/academics')

    from backoffice.views import backoffice as backoffice_blueprint
    app.register_blueprint(backoffice_blueprint, url_prefix='/backoffice')

    db.init_app(app)
    flask_bcrypt.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    admin.init_app(app)

    from models import (Department, SystemRole, ForumRole,
            AcademicPosition, FacultyInfo, RoomDirectory, Building,
            Job, Contact, Education, Degree, Title,
            HealthRegion, GeoRegion, Province, Amphur,
            LabAddress, Hospital, Lab, LabPhone, LabFax,
            # User, UserType,
            )
    from eqa.models import QACustomerCode, QAProgram, OTPCode
    from research.models import (ScopusAffiliation, ScopusAuthor,
                                    ScopusAbstract)

    # admin.add_view(UserModelView(User, db.session))
    admin.add_view(BaseModelView(Department, db.session))
    admin.add_view(BaseModelView(SystemRole, db.session))
    admin.add_view(BaseModelView(ForumRole, db.session))
    admin.add_view(BaseModelView(AcademicPosition, db.session))
    admin.add_view(BaseModelView(FacultyInfo, db.session))
    admin.add_view(BaseModelView(Building, db.session))
    admin.add_view(BaseModelView(RoomDirectory, db.session))
    admin.add_view(BaseModelView(Job, db.session))
    admin.add_view(BaseModelView(Contact, db.session))
    admin.add_view(BaseModelView(Education, db.session))
    admin.add_view(BaseModelView(Degree, db.session))
    admin.add_view(BaseModelView(Title, db.session))
    admin.add_view(BaseModelView(HealthRegion, db.session))
    admin.add_view(BaseModelView(GeoRegion, db.session))
    admin.add_view(BaseModelView(Province, db.session))
    admin.add_view(BaseModelView(Amphur, db.session))
    admin.add_view(BaseModelView(LabAddress, db.session))
    admin.add_view(BaseModelView(Hospital, db.session))
    admin.add_view(BaseModelView(Lab, db.session))
    admin.add_view(BaseModelView(LabPhone, db.session))
    admin.add_view(BaseModelView(LabFax, db.session))
    admin.add_view(BaseModelView(QACustomerCode, db.session))
    admin.add_view(BaseModelView(QAProgram, db.session))
    admin.add_view(BaseModelView(OTPCode, db.session))
    admin.add_view(BaseModelView(ScopusAffiliation, db.session))
    admin.add_view(BaseModelView(ScopusAuthor, db.session))
    admin.add_view(BaseModelView(ScopusAbstract, db.session))
    # admin.add_view(BaseModelView(UserType, db.session))

    return app

from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
