from logging import getLogger

from elasticsearch import Elasticsearch
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from app.main.config import config_by_name

LOG = getLogger(__name__)

LOG.info('configured logger!')

db = SQLAlchemy()
flask_bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__, template_folder="../static/templates")
    app.config.from_object(config_by_name[config_name])
    LOG.info('app loaded with configuration!')

    app.app_context().push()
    LOG.info('application context pushed')

    db.init_app(app)
    LOG.info('database initialized successfully!')

    flask_bcrypt.init_app(app)
    LOG.info('flask encryption initialized successfully!')

    login_manager.init_app(app)
    LOG.info('Flask-Login set up successfully!')

    CORS(app)
    LOG.info("Flask-CORS set up succesfully!")

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']])
    LOG.info("Elasticsearch set up successfully!")

    jwt = JWTManager(app)
    LOG.info("JWT Set Up!")

    return app
