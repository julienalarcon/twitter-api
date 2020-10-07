# pylint: disable=missing-docstring

from flask import Flask

def create_app():
    app = Flask(__name__)

    from .main.controllers import main
    app.register_blueprint(main)

    return app
