from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
from flask.ext.bootstrap import Bootstrap

db = SQLAlchemy()
flask_bcrypt = Bcrypt()
login_manager = LoginManager()
bootstrap = Bootstrap()

def create_app(config=None):
    app = Flask(__name__)

    # configure the app here
    if config:
        pass
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../mtweb.db'
        app.config['SECRET_KEY'] = 'thegodfather'

    from services.views import services as services_blueprint
    app.register_blueprint(services_blueprint, url_prefix='/services')

    from eqa.views import eqa as eqa_blueprint
    app.register_blueprint(eqa_blueprint, url_prefix='/eqa')

    from auth.views import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from main.views import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='')

    db.init_app(app)
    flask_bcrypt.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)

    return app

from app.auth.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
