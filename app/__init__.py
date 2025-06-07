from flask import Flask


def create_app():
    app = Flask(__name__)
    # app.config.from_object('config.Config')  # Only if you have a config.py

    from .api import api_bp
    app.register_blueprint(api_bp)

    return app