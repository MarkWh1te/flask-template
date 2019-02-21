from flask import request, make_response, jsonify
from flask.views import MethodView
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from app import bcrypt, db
from app.models.user import User


from . import auth


@auth.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if not User.check_credentials(username, password):
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200



@auth.route("/register", methods=["POST"])
def post():
    # get the post data
    post_data = request.get_json()
    print(post_data)
    # check if user already exists
    user = User.query.filter_by(email=post_data.get('email')).first()
    if not user:
        user = User(
            email=post_data.get('email'),
            password=post_data.get('password')
        )

        # insert the user
        db.session.add(user)
        db.session.commit()
        # generate the auth token
        access_token = create_access_token(identity=user.email)
        responseObject = {
            'status': 'success',
            'message': 'Successfully registered.',
            'access_token': access_token
        }
        return make_response(jsonify(responseObject)), 201

    else:
        responseObject = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return make_response(jsonify(responseObject)), 202


@auth.route("/status", methods=["GET"])
@jwt_required
def status():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
