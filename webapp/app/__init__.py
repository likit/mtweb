from flask import Flask

def create_app(config=None):
    app = Flask(__name__)

    # configure the app here
    if config:
        pass

    from services.views import services as services_blueprint
    app.register_blueprint(services_blueprint, url_prefix='/services')

    return app
