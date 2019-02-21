import jwt
import datetime
from flask import current_app
from app import db, bcrypt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    confirmed_mail = db.Column(db.Boolean, default=False)


    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def check_credentials(email, passwd):
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, passwd):
            return True
        return False