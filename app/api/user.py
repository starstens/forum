from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, current_user

from app.extension import db, jwt
from app.services.user import UserORMHandler

user_blueprint = Blueprint("user", __name__, url_prefix="/user")


@jwt.user_identity_loader
def user_identity_lookup(user_id):
    return user_id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return identity


@user_blueprint.route("/login/", methods=["POST"])
def login():
    user_id = request.form.get("user_id")
    password = request.form.get("password")
    if result := UserORMHandler(db.session).login(user_id, password):
        access_token = create_access_token(identity=user_id)
        if result["user_group"] > 1:
            return jsonify({
                "msg_condition": "admin",
                "access_token": access_token
            })
        return jsonify({
            "msg_condition": "login successful",
            "access_token": access_token
        })
    else:
        return jsonify({
            "msg": "Bad username or password"
        }), 401


@user_blueprint.route("/add", methods=["POST"])
def add():
    UserORMHandler(db.session).add(request.get_json())
    return jsonify({
        "msg_condition": "success"
    })


@user_blueprint.route("/me", methods=["GET", "DELETE"])
@jwt_required()
def get_and_delete():
    if request.method == "GET":
        print(type(current_user))
        user = UserORMHandler(db.session).get_detail(current_user)
        return jsonify(
            user.to_dict() if user is not None else {
                "msg_condition": "The user do not exist"
            }
        )
    elif request.method == "DELETE":
        UserORMHandler(db.session).delete(user_id=current_user)
        return jsonify({
            "msg_condition": "success"
        })


@user_blueprint.route("/", methods=["GET"])
@jwt_required()
def get():
    return jsonify({
        "user_list": [item.to_dict() for item in UserORMHandler(db.session).get_all()]
    })


@user_blueprint.route("/delete", methods=["POST"])
@jwt_required()
def delete():
    data = request.get_json()
    if "users" not in data:
        return jsonify({
            "msg_condition": "Message Format Error"
        })
    UserORMHandler(db.session).delete_args(data["users"])
    return jsonify({
        "msg_condition": "success"
    })


@user_blueprint.route("/update", methods=["POST"])
@jwt_required()
def update():
    data = request.get_json()
    print(data)
    if "users" not in data:
        return jsonify({
            "msg_condition": "格式错误"
        })
    data = data["users"]
    UserORMHandler(db.session).update(data)
    return jsonify({
        "msg_condition": "success"
    })
