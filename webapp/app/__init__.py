from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
from flask.ext.bootstrap import Bootstrap
from config import config

db = SQLAlchemy()
flask_bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

bootstrap = Bootstrap()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

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

    db.init_app(app)
    flask_bcrypt.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)

    return app

from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
