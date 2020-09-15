from . import auth_bp
from . import db
from flask import jsonify, request
from flask_jwt_extended import create_access_token
import hashlib


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Bad request."}), 400
    username = data.get("username", None)
    password = data.get("password", None)
    name = data.get("name", None)

    if not username:
        return jsonify({"message": "Missing username."}), 400
    elif not password:
        return jsonify({"message", "Missing password."}), 400
    elif not name:
        return jsonify({"message", "Missing name."}), 400

    if db.username_exists(username):
        return jsonify({"message": "Username already exists."}), 400

    hashed_password = hashlib.sha256(password.encode("utf8")).hexdigest()
    db.create_user(username, hashed_password, name)
    return jsonify({"message": "User created."}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"message": "Request body is not json"}), 400

    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username:
        return jsonify({"message": "Missing username"}), 400
    if not password:
        return jsonify({"message": "Missing password."}), 400

    hashed_password = hashlib.sha256(password.encode("utf8")).hexdigest()
    user = db.authenticate_user(username, hashed_password)
    if not user:
        return jsonify({"message": "User does not exist"}), 401

    return jsonify({"access_token": create_access_token(identity=username)}), 200