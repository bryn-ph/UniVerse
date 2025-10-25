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


# ---------- POST /discussions ----------
@discussion_bp.route("/discussions", methods=["POST"])
def create_discussion():
    """Create a new discussion"""
    data = request.get_json()
    title = data.get("title")
    body = data.get("body")
    user_id = data.get("user_id")  # (for now, pass in frontend)
    class_id = data.get("class_id")

    if not all([title, body, user_id, class_id]):
        return jsonify({"error": "Missing required fields"}), 400

    discussion = Discussion(
        id=uuid.uuid4(),
        title=title,
        body=body,
        user_id=user_id,
        class_id=class_id
    )

    db.session.add(discussion)
    db.session.commit()

    return jsonify({
        "id": str(discussion.id),
        "title": discussion.title,
        "body": discussion.body,
        "class_id": str(discussion.class_id),
        "created_at": discussion.created_at.isoformat(),
    }), 201


# ---------- GET /discussions/<id> ----------
@discussion_bp.route("/discussions/<uuid:discussion_id>", methods=["GET"])
def get_discussion(discussion_id):
    """Get a single discussion and its replies"""
    discussion = Discussion.query.get(discussion_id)
    if not discussion:
        return jsonify({"error": "Not found"}), 404

    replies = [
        {
            "id": str(r.id),
            "body": r.body,
            "author": r.user.name,
            "created_at": r.created_at.isoformat(),
        }
        for r in discussion.replies
    ]

    return jsonify({
        "id": str(discussion.id),
        "title": discussion.title,
        "body": discussion.body,
        "author": discussion.user.name,
        "class": discussion.class_.name,
        "university": discussion.class_.university.name,
        "created_at": discussion.created_at.isoformat(),
        "replies": replies
    })


# ---------- POST /discussions/<id>/replies ----------
@discussion_bp.route("/discussions/<uuid:discussion_id>/replies", methods=["POST"])
def add_reply(discussion_id):
    """Add a reply to a discussion"""
    data = request.get_json()
    body = data.get("body")
    user_id = data.get("user_id")

    if not all([body, user_id]):
        return jsonify({"error": "Missing fields"}), 400

    reply = Reply(
        id=uuid.uuid4(),
        body=body,
        user_id=user_id,
        discussion_id=discussion_id
    )
    db.session.add(reply)
    db.session.commit()

    return jsonify({
        "id": str(reply.id),
        "body": reply.body,
        "created_at": reply.created_at.isoformat(),
        "author": reply.user.name
    }), 201
