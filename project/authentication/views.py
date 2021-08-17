from flask import Blueprint, make_response, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    create_refresh_token,
)

from project.authentication.models import User
from project import bcrypt, db


auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@auth_blueprint.post("/login")
def post_login():
    post_data = request.get_json()
    try:
        user = User.query.filter_by(username=post_data.get("username")).first()
        if user and bcrypt.check_password_hash(
            user.password, post_data.get("password")
        ):
            auth_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            if auth_token:
                response = {
                    "status": "success",
                    "message": "Başarıyla giriş yapıldı.",
                    "auth_token": auth_token,
                    "refresh_token": refresh_token,
                }
                return make_response(jsonify(response)), 200
        else:
            response = {"status": "fail", "message": "Kullanıcı bulunmamaktadır."}
            return make_response(jsonify(response)), 404

    except Exception as e:
        print(e)
        response = {"status": "fail", "message": "Try again"}
        return make_response(jsonify(response)), 500


@auth_blueprint.post("/register")
def post_register():
    post_data = request.get_json()

    user = User.query.filter_by(username=post_data.get("username")).first()
    if not user:
        try:
            user = User(
                username=post_data.get("username"), password=post_data.get("password")
            )
            db.session.add(user)
            db.session.commit()

            response = {
                "status": "success",
                "message": "Kullanıcı başarı ile oluşturuldu.",
            }
            return make_response(jsonify(response)), 201

        except Exception as e:
            print(e)
            response = {"status": "fail", "message": "Bir hata oluştu."}
            return make_response(jsonify(response)), 500
    else:
        response = {"status": "fail", "message": "Kullanıcı adı bulunmaktadır."}
        return make_response(jsonify(response)), 409


@auth_blueprint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    try:
        identity = get_jwt_identity()
        auth_token = create_access_token(identity=identity)
        response = {
            "status": "success",
            "message": "Başarıyla giriş yapıldı.",
            "auth_token": auth_token,
        }
        return make_response(jsonify(response)), 201
    except Exception as e:
        print(e)
        response = {"status": "fail", "message": "Bir hata oluştu."}
        return make_response(jsonify(response)), 500
