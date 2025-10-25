from flask import Blueprint, request, jsonify
from models import db, University, User, Class
from sqlalchemy import func
import uuid

university_bp = Blueprint("university", __name__)

# ---------- GET /universities ----------
@university_bp.route("/universities", methods=["GET"])
def get_universities():
    """Get all universities"""
    search = request.args.get("q")
    
    q = University.query
    
    if search:
        q = q.filter(University.name.ilike(f"%{search}%"))
    
    universities = q.order_by(University.name.asc()).all()
    
    return jsonify([
        {
            "id": str(u.id),
            "name": u.name,
            "user_count": len(u.users),
            "class_count": len(u.classes)
        }
        for u in universities
    ])

# ---------- GET /universities/<id> ----------
@university_bp.route("/universities/<university_id>", methods=["GET"])
def get_university(university_id):
    """Get a specific university by ID"""
    try:
        university = University.query.get(uuid.UUID(university_id))
        if not university:
            return jsonify({"error": "University not found"}), 404
        
        return jsonify({
            "id": str(university.id),
            "name": university.name,
            "user_count": len(university.users),
            "class_count": len(university.classes),
            "classes": [
                {
                    "id": str(c.id),
                    "name": c.name,
                    "tag_count": len(c.tags)
                }
                for c in university.classes
            ]
        })
    except ValueError:
        return jsonify({"error": "Invalid UUID format"}), 400

# ---------- GET /universities/<id>/classes ----------
@university_bp.route("/universities/<university_id>/classes", methods=["GET"])
def get_university_classes(university_id):
    """Get all classes for a specific university"""
    try:
        university = University.query.get(uuid.UUID(university_id))
        if not university:
            return jsonify({"error": "University not found"}), 404
        
        return jsonify([
            {
                "id": str(c.id),
                "name": c.name,
                "university_id": str(c.university_id),
                "discussion_count": len(c.discussions),
                "tags": [
                    {
                        "id": str(t.id),
                        "name": t.name
                    }
                    for t in c.tags
                ]
            }
            for c in university.classes
        ])
    except ValueError:
        return jsonify({"error": "Invalid UUID format"}), 400

# ---------- GET /universities/<id>/users ----------
@university_bp.route("/universities/<university_id>/users", methods=["GET"])
def get_university_users(university_id):
    """Get all users for a specific university"""
    try:
        university = University.query.get(uuid.UUID(university_id))
        if not university:
            return jsonify({"error": "University not found"}), 404
        
        return jsonify([
            {
                "id": str(u.id),
                "name": u.name,
                "email": u.email,
                "created_at": u.created_at.isoformat(),
                "discussion_count": len(u.discussions),
                "reply_count": len(u.replies)
            }
            for u in university.users
        ])
    except ValueError:
        return jsonify({"error": "Invalid UUID format"}), 400

# ---------- GET /universities/<id>/stats ----------
@university_bp.route("/universities/<university_id>/stats", methods=["GET"])
def get_university_stats(university_id):
    """Get statistics for a specific university"""
    try:
        university = University.query.get(uuid.UUID(university_id))
        if not university:
            return jsonify({"error": "University not found"}), 404
        
        # Calculate total discussions across all classes
        total_discussions = sum(len(c.discussions) for c in university.classes)
        
        return jsonify({
            "id": str(university.id),
            "name": university.name,
            "user_count": len(university.users),
            "class_count": len(university.classes),
            "total_discussions": total_discussions
        })
    except ValueError:
        return jsonify({"error": "Invalid UUID format"}), 400

# ---------- POST /universities ----------
@university_bp.route("/universities", methods=["POST"])
def create_university():
    """Create a new university"""
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    if "name" not in data:
        return jsonify({"error": "Missing required field: name"}), 400
    
    try:
        # Check if university with this name already exists
        existing = University.query.filter_by(name=data["name"]).first()
        if existing:
            return jsonify({"error": "University with this name already exists"}), 409
        
        # Create university
        university = University(name=data["name"])
        
        db.session.add(university)
        db.session.commit()
        
        return jsonify({
            "id": str(university.id),
            "name": university.name,
            "message": "University created successfully"
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ---------- PUT /universities/<id> ----------
@university_bp.route("/universities/<university_id>", methods=["PUT"])
def update_university(university_id):
    """Update a university"""
    try:
        university = University.query.get(uuid.UUID(university_id))
        if not university:
            return jsonify({"error": "University not found"}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Update name if provided
        if "name" in data:
            # Check if another university has this name
            existing = University.query.filter(
                University.name == data["name"],
                University.id != uuid.UUID(university_id)
            ).first()
            if existing:
                return jsonify({"error": "University with this name already exists"}), 409
            
            university.name = data["name"]
        
        db.session.commit()
        
        return jsonify({
            "id": str(university.id),
            "name": university.name,
            "message": "University updated successfully"
        })
        
    except ValueError:
        return jsonify({"error": "Invalid UUID format"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ---------- DELETE /universities/<id> ----------
@university_bp.route("/universities/<university_id>", methods=["DELETE"])
def delete_university(university_id):
    """Delete a university (will cascade delete all related users, classes, discussions, and replies)"""
    try:
        university = University.query.get(uuid.UUID(university_id))
        if not university:
            return jsonify({"error": "University not found"}), 404
        
        university_name = university.name
        
        db.session.delete(university)
        db.session.commit()
        
        return jsonify({
            "message": f"University '{university_name}' deleted successfully"
        }), 200
        
    except ValueError:
        return jsonify({"error": "Invalid UUID format"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

