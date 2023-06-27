from flask import Blueprint, request, jsonify

from app.extension import db
from app.services.user import UserORMHandler

user_blueprint = Blueprint("user", __name__, url_prefix="/user")


@user_blueprint.route("/<int:user_id>", methods=["GET", "DELETE"])
def get_and_delete(user_id: int):
    if request.method == "GET":
        user = UserORMHandler(db.session).get(user_id)
        return jsonify(
            user.to_dict() if user is not None else {
                "msg_condition": "The user do not exist"
            }
        )
    elif request.method == "DELETE":
        UserORMHandler(db.session).delete(user_id=user_id)
        return jsonify({
            "msg_condition": "success"
        })



@user_blueprint.route("/add", methods=["POST"])
def add():
    data = request.get_json()
    if "users" not in data:
        return jsonify({
            "msg_condition": "格式错误"
        })
    data = data["users"]
    UserORMHandler(db.session).add(data)
    return jsonify({
        "msg_condition": "success"
    })


@user_blueprint.route("/delete", methods=["POST"])
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
