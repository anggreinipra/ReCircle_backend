from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from app.database import db
from app.models.community import CommunityPost

community_ns = Namespace('community', description='Community post operations')

post_model = community_ns.model('CommunityPost', {
    'title': fields.String(required=True, description='Title of the post'),
    'content': fields.String(required=True, description='Content of the post'),
    'type': fields.String(default='article', description='Type of post (article, tip, etc.)')
})

@community_ns.route("/")
class CommunityPostList(Resource):
    def get(self):
        posts = CommunityPost.query.all()
        return [{
            "id": p.id,
            "title": p.title,
            "content": p.content,
            "type": p.type,
            "author_id": p.author_id,
            "created_at": p.created_at
        } for p in posts]

    @community_ns.expect(post_model)
    @jwt_required()
    def post(self):
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

        return {"message": "Post created"}, 201

@community_ns.route("/<int:post_id>")
@community_ns.param('post_id', 'The post identifier')
class CommunityPostDetail(Resource):
    @community_ns.expect(post_model)
    @jwt_required()
    def put(self, post_id):
        current_user = get_jwt_identity()
        post = CommunityPost.query.get_or_404(post_id)

        if post.author_id != current_user["id"]:
            return {"message": "Unauthorized"}, 403

        data = request.get_json()
        post.title = data.get("title", post.title)
        post.content = data.get("content", post.content)
        post.type = data.get("type", post.type)

        db.session.commit()
        return {"message": "Post updated"}

    @jwt_required()
    def delete(self, post_id):
        current_user = get_jwt_identity()
        post = CommunityPost.query.get_or_404(post_id)

        if post.author_id != current_user["id"]:
            return {"message": "Unauthorized"}, 403

        db.session.delete(post)
        db.session.commit()
        return {"message": "Post deleted"}
