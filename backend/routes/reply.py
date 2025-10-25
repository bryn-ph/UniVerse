from flask_smorest import Blueprint
from models import db, Reply, User, Discussion
from schemas import ReplySchema, ReplyCreateSchema, ReplyUpdateSchema
import uuid

reply_bp = Blueprint("reply", __name__, url_prefix="/api/replies")

# ---------- GET /replies ----------
@reply_bp.route("/", methods=["GET"])
@reply_bp.response(200, ReplySchema(many=True))
def get_replies():
    """List all replies (optionally filtered by discussion_id or user_id)"""
    from flask import request
    discussion_id = request.args.get("discussion_id")
    user_id = request.args.get("user_id")

    q = Reply.query.join(Reply.user).join(Reply.discussion)
    if discussion_id:
        q = q.filter(Reply.discussion_id == discussion_id)
    if user_id:
        q = q.filter(Reply.user_id == user_id)

    return q.order_by(Reply.created_at.asc()).all()


# ---------- POST /replies ----------
@reply_bp.route("/", methods=["POST"])
@reply_bp.arguments(ReplyCreateSchema)
@reply_bp.response(201, ReplySchema)
def create_reply(data):
    """Create a new reply"""
    user = User.query.get(data["user_id"])
    discussion = Discussion.query.get(data["discussion_id"])
    if not user or not discussion:
        return {"error": "User or discussion not found"}, 404

    reply = Reply(
        id=uuid.uuid4(),
        body=data["body"],
        user_id=data["user_id"],
        discussion_id=data["discussion_id"],
    )
    db.session.add(reply)
    db.session.commit()
    return reply


# ---------- PUT /replies/<id> ----------
@reply_bp.route("/<uuid:reply_id>", methods=["PUT"])
@reply_bp.arguments(ReplyUpdateSchema)
@reply_bp.response(200, ReplySchema)
def update_reply(data, reply_id):
    """Update reply body"""
    reply = Reply.query.get_or_404(reply_id)
    if "body" in data:
        reply.body = data["body"]
    db.session.commit()
    return reply


# ---------- DELETE /replies/<id> ----------
@reply_bp.route("/<uuid:reply_id>", methods=["DELETE"])
@reply_bp.response(204)
def delete_reply(reply_id):
    """Delete a reply"""
    reply = Reply.query.get_or_404(reply_id)
    db.session.delete(reply)
    db.session.commit()
    return {}
