from flask import Blueprint, request, jsonify
from models import db, Discussion, User, Class, Reply
from sqlalchemy import func
import uuid

discussion_bp = Blueprint("discussion", __name__)

# ---------- GET /discussions ----------
@discussion_bp.route("/discussions", methods=["GET"])
def get_discussions():
    """Get all discussions (optionally filtered by class or university)"""
    class_id = request.args.get("class_id")
    university_id = request.args.get("university_id")
    search = request.args.get("q")

    q = Discussion.query.join(Discussion.user).join(Discussion.class_)
    if class_id:
        q = q.filter(Discussion.class_id == class_id)
    if university_id:
        q = q.filter(Class.university_id == university_id)
    if search:
        q = q.filter(
            db.or_(
                Discussion.title.ilike(f"%{search}%"),
                Discussion.body.ilike(f"%{search}%")
            )
        )

    discussions = q.order_by(Discussion.created_at.desc()).all()

    return jsonify([
        {
            "id": str(d.id),
            "title": d.title,
            "body": d.body[:180] + "..." if len(d.body) > 180 else d.body,
            "created_at": d.created_at.isoformat(),
            "author": d.user.name,
            "university": d.user.university.name,
            "class": d.class_.name,
            "reply_count": len(d.replies)
        }
        for d in discussions
    ])

