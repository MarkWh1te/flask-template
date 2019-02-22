from flask import request, make_response, jsonify, current_app
from flask.views import MethodView
from flask_mail import Message
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, decode_token

from app import bcrypt, db, mail
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

    user = User.get_user(username)
    if not user:
        return jsonify({"msg": "Bad username or password"}), 401
    if not user.check_credentials(password):
        return jsonify({"msg": "Bad username or password"}), 401

    if not user.confirmed_mail:
        return jsonify({"msg": "Need to confirm email"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

@auth.route("/register", methods=["POST"])
def post():
    post_data = request.get_json()
    email = post_data.get('email')
    password = post_data.get('password')

    user = User.query.filter_by(email=post_data.get('email')).first()
    if user:
        return jsonify({"msg": "Fail", "reason": "User already exists"}), 202
    if not email.endswith(current_app.config["REQUIRED_DOMAIN"]):
        return jsonify({"msg": "Fail", "reason": "Not authorized"}), 202
    
    user = User(email=email,password=password)
    db.session.add(user)
    db.session.commit()

    # generate the auth token
    access_token = create_access_token(identity=user.email)
    msg = text_confirm_email(current_app.config["CONFIRM_HOST"], access_token)
    mail.send_msg(current_app.config["MAIL_SENDER"], email, "Confirmar email", msg)

    return jsonify({"status": 'success'}), 201


@auth.route("/confirm", methods=["GET"])
def confirm_email():
    token = request.args.get('confirm')
    values = decode_token(token, allow_expired=True)
    if values["exp"] - values["iat"] > 10800:  # 3 horas
        return jsonify({"status": 'Fail', "msg": "Token expired"})

    user = User.get_user(values["identity"])
    user.set_confirmed()
    access_token = create_access_token(identity=values["identity"])
    return jsonify({"access_token": access_token})


@auth.route("/status", methods=["GET"])
@jwt_required
def status():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


def text_confirm_email(host, access_token):
    text = f"""\
    Você está recebendo este email pois solicitou o cadastro num aplicacao.
    Para completar o cadastro acesse o link abaixo:

    http://{host}/auth/confirm?confirm={access_token}
    """
    return text
