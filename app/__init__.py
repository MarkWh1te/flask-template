import os
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from app.shared.sendgrid_cli.sendgrid_flask import SendgridService

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
jwt = JWTManager()
mail = SendgridService()


def create_app(mode):
    app = Flask(__name__)
    CORS(app, resources={r"*": {"origins": "*"}})
    os.environ["CONFIG"] = config[mode]
    app.config.from_envvar("CONFIG")
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app


config = {
    "dev": "configurations/development.cfg",
    "test": "configurations/testing.cfg"
}