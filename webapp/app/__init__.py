from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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

    return app
