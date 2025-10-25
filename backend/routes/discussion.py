from flask_smorest import Blueprint
from models import db, Discussion, Class
from schemas import DiscussionSchema, DiscussionCreateSchema, DiscussionUpdateSchema, DiscussionQuerySchema
from sqlalchemy import or_
import uuid

discussion_bp = Blueprint("discussion", __name__, url_prefix="/api/discussions")

# ---------- GET /discussions ----------
@discussion_bp.route("/", methods=["GET"])
@discussion_bp.arguments(DiscussionQuerySchema, location="query")
@discussion_bp.response(200, DiscussionSchema(many=True))
def get_discussions(query_args):
    """Get all discussions (optionally filtered by class, university, user, or class group)"""
    class_id = query_args.get("class_id")
    university_id = query_args.get("university_id")
    user_id = query_args.get("user_id")
    class_group_id = query_args.get("class_group_id")
    search = query_args.get("q")

    q = Discussion.query.join(Discussion.user).join(Discussion.class_)
    if class_id:
        q = q.filter(Discussion.class_id == class_id)
    if university_id:
        q = q.filter(Class.university_id == university_id)
    if user_id:
        q = q.filter(Discussion.user_id == user_id)
    if class_group_id:
        # Get all classes in this group and filter discussions by those class IDs
        q = q.filter(Class.class_group_id == class_group_id)
    if search:
        q = q.filter(
            or_(
                Discussion.title.ilike(f"%{search}%"),
                Discussion.body.ilike(f"%{search}%")
            )
        )

    return q.order_by(Discussion.created_at.desc()).all()


# ---------- POST /discussions ----------
@discussion_bp.route("/", methods=["POST"])
@discussion_bp.arguments(DiscussionCreateSchema)
@discussion_bp.response(201, DiscussionSchema)
def create_discussion(data):
    """Create a new discussion"""
    discussion = Discussion(
        id=uuid.uuid4(),
        title=data["title"],
        body=data["body"],
        user_id=data["user_id"],
        class_id=data["class_id"],
    )
    db.session.add(discussion)
    db.session.commit()
    return discussion


# ---------- GET /discussions/<id> ----------
@discussion_bp.route("/<uuid:discussion_id>", methods=["GET"])
@discussion_bp.response(200, DiscussionSchema)
def get_discussion(discussion_id):
    """Get a discussion by ID"""
    return Discussion.query.get_or_404(discussion_id)


# ---------- GET /discussions/<id>/replies ----------
@discussion_bp.route("/<uuid:discussion_id>/replies", methods=["GET"])
@discussion_bp.response(200)
def get_discussion_replies(discussion_id):
    """Get replies for a discussion (redirect to /api/replies?discussion_id=<id>)"""
    return {"message": "Use GET /api/replies?discussion_id={} to get replies".format(discussion_id)}
