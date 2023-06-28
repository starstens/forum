from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.extension import db
from app.services.post import PostORMHandler, CommentORMHandler, CheckORMHandler

post_blueprint = Blueprint("post", __name__, url_prefix="/post")


@post_blueprint.route("/", methods=["POST"])
@jwt_required()
def add():
    PostORMHandler(db.session).add(request.get_json())
    return jsonify({
        "msg_condition": "success"
    })


@post_blueprint.route("/comment/add", methods=["POST"])
def add_comment():
    CommentORMHandler(db.session).add(request.get_json())
    return jsonify({
        "msg_condition": "success"
    })


@post_blueprint.route("/<int:post_id>", methods=["DELETE"])
@jwt_required()
def delete_post(post_id: int):
    PostORMHandler(db.session).check(post_id, False, type="帖子")
    CheckORMHandler(db.session).add({
        "examine_state": 2,
        "type": "帖子",
        "checked_id": post_id
    })
    return jsonify({
        "msg_condition": "success"
    })


@post_blueprint.route("/comment/<int:comment_id>", methods=["DELETE"])
@jwt_required()
def delete_comment(comment_id: int):
    PostORMHandler(db.session).check(comment_id, False, type="评论")
    CheckORMHandler(db.session).add({
        "examine_state": 2,
        "type": "评论",
        "checked_id": comment_id
    })
    return jsonify({
        "msg_condition": "success"
    })


@post_blueprint.route("/home", methods=["GET"])
@jwt_required()
def get_post_home():
    post_list = PostORMHandler(db.session).get_post_home()
    return jsonify([
        item.to_dict() for item in post_list
    ])


@post_blueprint.route("/<int:post_id>", methods=["GET"])
@jwt_required()
def get_post(post_id: int):
    post, comment_list = CommentORMHandler(db.session).get(post_id=post_id)
    return jsonify(
        {
            "msg_condition": "success",
            "post": [item.to_dict() for item in post],
            "comment": [item.to_dict() for item in comment_list]
        } if post and comment_list else {
            "msg_condition": "The post do not exist"
        })


@post_blueprint.route("/check", methods=["GET"])
@jwt_required()
def get_check():
    check = [item.to_dict() for item in PostORMHandler(db.session).get_check()]
    for item in check:
        item["type"] = "title" \
            if "post_title" in item else "comment"
        item["content"] = item.pop("post_title") \
            if "post_title" in item else item.pop("comment_content")
    return jsonify(
        {
            "check": check
        }
    )


@post_blueprint.route("/check/<post_id>", methods=["GET"])
@jwt_required()
def check_post(post_id):
    PostORMHandler(db.session).check(post_id, True, type="帖子")
    CheckORMHandler(db.session).add({
        "examine_state": 0,
        "type": "帖子",
        "checked_id": post_id
    })


@post_blueprint.route("comment/check/<comment_id>", methods=["GET"])
@jwt_required()
def check_comment(comment_id):
    PostORMHandler(db.session).check(comment_id, True, type="评论")
    CheckORMHandler(db.session).add({
        "examine_state": 0,
        "type": "评论",
        "checked_id": comment_id
    })
