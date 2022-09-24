"""Main app initialization."""

import logging
import os
import sys
import flask
import openai

from flask import Flask
from flask_mail import Mail

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)

from src.db_models import db_session


def create_app():
    logging.basicConfig(filename='record.log', level=logging.DEBUG,
                        format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

    app = Flask(__name__)
    mail = Mail(app)


    """Configure Flask app."""
    print("Configuring Flask app:")
    app.config.from_object(os.environ['APP_SETTINGS'])

    # Configure OpenAI
    openai.api_key = app.config.get('OPENAI_API_KEY')
    if not openai.api_key:
        app.logger.critical('OpenAi API key was not Found')
        return flask.abort(404)
    print("Configured OpenAI API key.")



    db_file = app.config.get('SQLALCHEMY_DATABASE_URI')
    db_session.global_init(db_file)
    print("DB setup completed.")
    print("", flush=True)

    # Configure Blueprints
    print("Registered blueprints")
    app.logger.info('Registering Blueprints')
    from src.views import home_views
    from src.views import account_views
    from src.views import app_views

    app.register_blueprint(account_views.blueprint)
    app.register_blueprint(home_views.blueprint)
    app.register_blueprint(app_views.blueprint)
    app.logger.info('Blueprints Registered')

    return app