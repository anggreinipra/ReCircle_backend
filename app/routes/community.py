from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.database import db
from app.models.community import CommunityPost

bp = Blueprint("community", __name__, url_prefix="/community")

@bp.route("/", methods=["GET"])
def get_posts():
    posts = CommunityPost.query.all()
    result = [{
        "id": p.id,
        "title": p.title,
        "content": p.content,
        "type": p.type,
        "author_id": p.author_id,
        "created_at": p.created_at
    } for p in posts]
    return jsonify(result)

@bp.route("/", methods=["POST"])
@jwt_required()
def create_post():
    current_user = get_jwt_identity()
    data = request.get_json()

    post = CommunityPost(
        title=data.get("title"),
        content=data.get("content"),
        type=data.get("type", "article"),
        author_id=current_user["id"]
    )

    db.session.add(post)
    db.session.commit()

    return jsonify({"message": "Post created"}), 201

@bp.route("/<int:post_id>", methods=["PUT"])
@jwt_required()
def update_post(post_id):
    current_user = get_jwt_identity()
    post = CommunityPost.query.get_or_404(post_id)

    if post.author_id != current_user["id"]:
        return jsonify({"message": "Unauthorized"}), 403

    data = request.get_json()
    post.title = data.get("title", post.title)
    post.content = data.get("content", post.content)
    post.type = data.get("type", post.type)

    db.session.commit()
    return jsonify({"message": "Post updated"})

@bp.route("/<int:post_id>", methods=["DELETE"])
@jwt_required()
def delete_post(post_id):
    current_user = get_jwt_identity()
    post = CommunityPost.query.get_or_404(post_id)

    if post.author_id != current_user["id"]:
        return jsonify({"message": "Unauthorized"}), 403

    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted"})
