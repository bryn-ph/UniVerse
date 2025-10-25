from flask_smorest import Blueprint
from models import db, Reply, User, Discussion
from schemas import ReplySchema
import uuid

reply_bp = Blueprint("reply", __name__, url_prefix="/api/replies")

# ---------- GET /replies ----------
@reply_bp.route("/", methods=["GET"])
@reply_bp.response(200, ReplySchema(many=True))
def get_replies():
    """List all replies (filterable by discussion_id or user_id)"""
    discussion_id = uuid.request.args.get("discussion_id")
    user_id = uuid.request.args.get("user_id")

    q = Reply.query.join(Reply.user).join(Reply.discussion)
    if discussion_id:
        q = q.filter(Reply.discussion_id == discussion_id)
    if user_id:
        q = q.filter(Reply.user_id == user_id)
    replies = q.order_by(Reply.created_at.asc()).all()

    for r in replies:
        r.author = r.user.name
        r.author_id = r.user_id
    return replies


# ---------- POST /replies ----------
@reply_bp.route("/", methods=["POST"])
@reply_bp.arguments(ReplySchema)
@reply_bp.response(201, ReplySchema)
def create_reply(data):
    """Create a reply"""
    user = User.query.get(data["author_id"])
    disc = Discussion.query.get(data["discussion_id"])
    if not user or not disc:
        return {"error": "User or Discussion not found"}, 404

    reply = Reply(
        id=uuid.uuid4(),
        body=data["body"],
        user_id=user.id,
        discussion_id=disc.id,
    )
    db.session.add(reply)
    db.session.commit()
    reply.author = user.name
    reply.author_id = user.id
    return reply


# ---------- PUT /replies/<id> ----------
@reply_bp.route("/<uuid:reply_id>", methods=["PUT"])
@reply_bp.arguments(ReplySchema(partial=True))
@reply_bp.response(200, ReplySchema)
def update_reply(data, reply_id):
    """Update a reply body"""
    reply = Reply.query.get_or_404(reply_id)
    if "body" in data:
        reply.body = data["body"]
    db.session.commit()
    reply.author = reply.user.name
    reply.author_id = reply.user.id
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
