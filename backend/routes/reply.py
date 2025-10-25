from flask import Blueprint, request, jsonify
from models import db, Reply, User, Discussion
from sqlalchemy import func
import uuid

reply_bp = Blueprint("reply", __name__)

# ---------- GET /replies ----------
@reply_bp.route("/replies", methods=["GET"])
def get_replies():
    """Get all replies (optionally filtered by discussion_id or user_id)"""
    discussion_id = request.args.get("discussion_id")
    user_id = request.args.get("user_id")
    
    q = Reply.query.join(Reply.user).join(Reply.discussion)
    
    if discussion_id:
        q = q.filter(Reply.discussion_id == discussion_id)
    if user_id:
        q = q.filter(Reply.user_id == user_id)
    
    replies = q.order_by(Reply.created_at.asc()).all()
    
    return jsonify([
        {
            "id": str(r.id),
            "body": r.body,
            "created_at": r.created_at.isoformat(),
            "author": r.user.name,
            "author_id": str(r.user_id),
            "discussion_id": str(r.discussion_id),
            "discussion_title": r.discussion.title
        }
        for r in replies
    ])

# ---------- GET /replies/<id> ----------
@reply_bp.route("/replies/<reply_id>", methods=["GET"])
def get_reply(reply_id):
    """Get a specific reply by ID"""
    try:
        reply = Reply.query.get(uuid.UUID(reply_id))
        if not reply:
            return jsonify({"error": "Reply not found"}), 404
        
        return jsonify({
            "id": str(reply.id),
            "body": reply.body,
            "created_at": reply.created_at.isoformat(),
            "author": reply.user.name,
            "author_id": str(reply.user_id),
            "author_email": reply.user.email,
            "discussion_id": str(reply.discussion_id),
            "discussion_title": reply.discussion.title
        })
    except ValueError:
        return jsonify({"error": "Invalid UUID format"}), 400

# ---------- POST /replies ----------
@reply_bp.route("/replies", methods=["POST"])
def create_reply():
    """Create a new reply"""
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    required_fields = ["body", "user_id", "discussion_id"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    try:
        # Validate UUIDs
        user_id = uuid.UUID(data["user_id"])
        discussion_id = uuid.UUID(data["discussion_id"])
        
        # Check if user and discussion exist
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        discussion = Discussion.query.get(discussion_id)
        if not discussion:
            return jsonify({"error": "Discussion not found"}), 404
        
        # Create reply
        reply = Reply(
            body=data["body"],
            user_id=user_id,
            discussion_id=discussion_id
        )
        
        db.session.add(reply)
        db.session.commit()
        
        return jsonify({
            "id": str(reply.id),
            "body": reply.body,
            "created_at": reply.created_at.isoformat(),
            "author": reply.user.name,
            "author_id": str(reply.user_id),
            "discussion_id": str(reply.discussion_id),
            "message": "Reply created successfully"
        }), 201
        
    except ValueError:
        return jsonify({"error": "Invalid UUID format"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ---------- PUT /replies/<id> ----------
@reply_bp.route("/replies/<reply_id>", methods=["PUT"])
def update_reply(reply_id):
    """Update a reply"""
    try:
        reply = Reply.query.get(uuid.UUID(reply_id))
        if not reply:
            return jsonify({"error": "Reply not found"}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Only allow updating the body
        if "body" in data:
            reply.body = data["body"]
        
        db.session.commit()
        
        return jsonify({
            "id": str(reply.id),
            "body": reply.body,
            "created_at": reply.created_at.isoformat(),
            "message": "Reply updated successfully"
        })
        
    except ValueError:
        return jsonify({"error": "Invalid UUID format"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ---------- DELETE /replies/<id> ----------
@reply_bp.route("/replies/<reply_id>", methods=["DELETE"])
def delete_reply(reply_id):
    """Delete a reply"""
    try:
        reply = Reply.query.get(uuid.UUID(reply_id))
        if not reply:
            return jsonify({"error": "Reply not found"}), 404
        
        db.session.delete(reply)
        db.session.commit()
        
        return jsonify({"message": "Reply deleted successfully"}), 200
        
    except ValueError:
        return jsonify({"error": "Invalid UUID format"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500