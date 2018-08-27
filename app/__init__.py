import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()


def create_app(mode):
    app = Flask(__name__)
    app.config.from_object(config[mode])
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app



class DevConf:
    SQLALCHEMY_DATABASE_URI =  f'sqlite:///{os.getcwd()}/escola.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "blablabl"

class TestConf:
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.getcwd()}/escola_test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "blablabl"

config = {
    "dev": DevConf,
    "test": TestConf
}