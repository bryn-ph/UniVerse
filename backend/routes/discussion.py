from flask_smorest import Blueprint
from flask import request
from models import db, Discussion, Reply, Class
from schemas import DiscussionSchema, ReplySchema
import uuid
from sqlalchemy import or_

discussion_bp = Blueprint("discussion", __name__, url_prefix="/api/discussions")

# ---------- GET /discussions ----------
@discussion_bp.route("/", methods=["GET"])
@discussion_bp.response(200, DiscussionSchema(many=True))
def get_discussions():
    """Get all discussions (optionally filtered by class or university)."""
    class_id = request.args.get("class_id")
    university_id = request.args.get("university_id")
    search = request.args.get("q")

    q = Discussion.query.join(Discussion.user).join(Discussion.class_)

    if class_id:
        q = q.filter(Discussion.class_id == class_id)
    if university_id:
        q = q.filter(Class.university_id == university_id)
    if search:
        q = q.filter(or_(
            Discussion.title.ilike(f"%{search}%"),
            Discussion.body.ilike(f"%{search}%")
        ))

    discussions = q.order_by(Discussion.created_at.desc()).all()

    # Enrich with computed fields
    for d in discussions:
        d.author = d.user.name
        d.university = d.user.university.name
        d.class_name = d.class_.name
        d.reply_count = len(d.replies)

    return discussions


# ---------- POST /discussions ----------
@discussion_bp.route("/", methods=["POST"])
@discussion_bp.arguments(DiscussionSchema)
@discussion_bp.response(201, DiscussionSchema)
def create_discussion(data):
    """Create a new discussion."""
    discussion = Discussion(
        id=uuid.uuid4(),
        title=data["title"],
        body=data["body"],
        user_id=data["user_id"],
        class_id=data["class_id"],
    )

    db.session.add(discussion)
    db.session.commit()

    # attach relationships for response
    discussion.author = discussion.user.name
    discussion.university = discussion.user.university.name
    discussion.class_name = discussion.class_.name
    discussion.reply_count = len(discussion.replies)
    return discussion


# ---------- GET /discussions/<id> ----------
@discussion_bp.route("/<uuid:discussion_id>", methods=["GET"])
@discussion_bp.response(200, DiscussionSchema)
def get_discussion(discussion_id):
    """Get a single discussion and its replies."""
    discussion = Discussion.query.get_or_404(discussion_id)
    discussion.author = discussion.user.name
    discussion.university = discussion.class_.university.name
    discussion.class_name = discussion.class_.name
    discussion.reply_count = len(discussion.replies)
    return discussion


# ---------- POST /discussions/<id>/replies ----------
@discussion_bp.route("/<uuid:discussion_id>/replies", methods=["POST"])
@discussion_bp.arguments(ReplySchema)
@discussion_bp.response(201, ReplySchema)
def add_reply(data, discussion_id):
    """Add a reply to a discussion."""
    reply = Reply(
        id=uuid.uuid4(),
        body=data["body"],
        user_id=data.get("user_id"),  # pass from frontend
        discussion_id=discussion_id
    )
    db.session.add(reply)
    db.session.commit()
    reply.author = reply.user.name
    return reply
