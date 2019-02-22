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
    admin = db.Column(db.Boolean, default=False)


    def __init__(self, email, password, admin=False, confirmed_mail=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.registered_on = datetime.datetime.now()
        self.admin = admin
        self.confirmed_mail = confirmed_mail

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def get_user(email):
        return User.query.filter_by(email=email).first()

    def set_confirmed(self):
        self.confirmed_mail = True
        db.session.add(self)
        db.session.commit()
        return True

    def check_credentials(self, passwd):
        if bcrypt.check_password_hash(self.password, passwd):
            return True
        return False
