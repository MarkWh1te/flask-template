from flask import jsonify
from app.models.user import User

from . import api

@api.route("/")
def hello():
    users = User.query.all()
    return jsonify({"msg": [u.username for u in users]})
