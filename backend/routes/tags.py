from flask import Blueprint, request, jsonify
from models import db, Tag, Class
from sqlalchemy import func
import uuid

tags_bp = Blueprint("tags", __name__)

# ---------- GET /tags ----------
@tags_bp.route("/tags", methods=["GET"])
def get_tags():
    """Get all tags with optional filtering and statistics"""
    search = request.args.get("q")
    sort_by = request.args.get("sort_by", "name")  
    limit = request.args.get("limit", type=int)
    
    q = Tag.query
    
    # Search filter
    if search:
        q = q.filter(Tag.name.ilike(f"%{search}%"))
    
    # Sorting
    if sort_by == "usage":
        # Sort by number of classes using this tag
        q = q.outerjoin(Tag.classes).group_by(Tag.id).order_by(func.count(Class.id).desc())
    elif sort_by == "name":
        q = q.order_by(Tag.name.asc())
    
    # Apply limit if specified
    if limit:
        q = q.limit(limit)
    
    tags = q.all()
    
    return jsonify([
        {
            "id": str(tag.id),
            "name": tag.name,
            "class_count": len(tag.classes)
        }
        for tag in tags
    ])


# ---------- GET /tags/<tag_id> ----------
@tags_bp.route("/tags/<string:tag_id>", methods=["GET"])
def get_tag(tag_id):
    """Get a specific tag with all its associated classes"""
    try:
        tag = Tag.query.get(uuid.UUID(tag_id))
        if not tag:
            return jsonify({"error": "Tag not found"}), 404
        
        return jsonify({
            "id": str(tag.id),
            "name": tag.name,
            "classes": [
                {
                    "id": str(c.id),
                    "name": c.name,
                    "university": c.university.name,
                    "university_id": str(c.university_id)
                }
                for c in tag.classes
            ],
            "class_count": len(tag.classes)
        })
    except ValueError:
        return jsonify({"error": "Invalid tag ID format"}), 400


# ---------- POST /tags ----------
@tags_bp.route("/tags", methods=["POST"])
def create_tag():
    """Create a new tag"""
    data = request.get_json()
    
    # Validation
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    name = data.get("name")
    if not name:
        return jsonify({"error": "Tag name is required"}), 400
    
    # Check if tag already exists (case-insensitive)
    existing_tag = Tag.query.filter(func.lower(Tag.name) == func.lower(name)).first()
    if existing_tag:
        return jsonify({
            "error": "Tag already exists",
            "existing_tag": {
                "id": str(existing_tag.id),
                "name": existing_tag.name
            }
        }), 409
    
    # Create new tag
    new_tag = Tag(name=name.strip())
    
    try:
        db.session.add(new_tag)
        db.session.commit()
        
        return jsonify({
            "id": str(new_tag.id),
            "name": new_tag.name,
            "class_count": 0
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create tag: {str(e)}"}), 500


# ---------- PUT /tags/<tag_id> ----------
@tags_bp.route("/tags/<string:tag_id>", methods=["PUT"])
def update_tag(tag_id):
    """Update a tag's name"""
    try:
        tag = Tag.query.get(uuid.UUID(tag_id))
        if not tag:
            return jsonify({"error": "Tag not found"}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        new_name = data.get("name")
        if not new_name:
            return jsonify({"error": "Tag name is required"}), 400
        
        # Check if new name already exists (excluding current tag)
        existing_tag = Tag.query.filter(
            func.lower(Tag.name) == func.lower(new_name),
            Tag.id != uuid.UUID(tag_id)
        ).first()
        
        if existing_tag:
            return jsonify({
                "error": "A tag with this name already exists",
                "existing_tag": {
                    "id": str(existing_tag.id),
                    "name": existing_tag.name
                }
            }), 409
        
        tag.name = new_name.strip()
        db.session.commit()
        
        return jsonify({
            "id": str(tag.id),
            "name": tag.name,
            "class_count": len(tag.classes)
        })
    except ValueError:
        return jsonify({"error": "Invalid tag ID format"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update tag: {str(e)}"}), 500


# ---------- DELETE /tags/<tag_id> ----------
@tags_bp.route("/tags/<string:tag_id>", methods=["DELETE"])
def delete_tag(tag_id):
    """Delete a tag (this will also remove it from all associated classes)"""
    try:
        tag = Tag.query.get(uuid.UUID(tag_id))
        if not tag:
            return jsonify({"error": "Tag not found"}), 404
        
        tag_name = tag.name
        class_count = len(tag.classes)
        
        db.session.delete(tag)
        db.session.commit()
        
        return jsonify({
            "message": f"Tag '{tag_name}' deleted successfully",
            "deleted_tag": {
                "id": tag_id,
                "name": tag_name,
                "affected_classes": class_count
            }
        }), 200
    except ValueError:
        return jsonify({"error": "Invalid tag ID format"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete tag: {str(e)}"}), 500


# ---------- GET /tags/<tag_id>/classes ----------
@tags_bp.route("/tags/<string:tag_id>/classes", methods=["GET"])
def get_tag_classes(tag_id):
    """Get all classes associated with a specific tag"""
    try:
        tag = Tag.query.get(uuid.UUID(tag_id))
        if not tag:
            return jsonify({"error": "Tag not found"}), 404
        
        university_id = request.args.get("university_id")
        
        classes = tag.classes
        
        # Filter by university if specified
        if university_id:
            classes = [c for c in classes if str(c.university_id) == university_id]
        
        return jsonify({
            "tag": {
                "id": str(tag.id),
                "name": tag.name
            },
            "classes": [
                {
                    "id": str(c.id),
                    "name": c.name,
                    "university": c.university.name,
                    "university_id": str(c.university_id),
                    "tags": [
                        {
                            "id": str(t.id),
                            "name": t.name
                        }
                        for t in c.tags
                    ]
                }
                for c in classes
            ],
            "total_classes": len(classes)
        })
    except ValueError:
        return jsonify({"error": "Invalid tag ID format"}), 400


# ---------- GET /tags/popular ----------
@tags_bp.route("/tags/popular", methods=["GET"])
def get_popular_tags():
    """Get most popular tags by usage count"""
    limit = request.args.get("limit", default=10, type=int)
    university_id = request.args.get("university_id")
    
    q = Tag.query.join(Tag.classes)
    
    if university_id:
        q = q.filter(Class.university_id == university_id)
    
    # Group by tag and count classes
    tags = (q.group_by(Tag.id)
            .order_by(func.count(Class.id).desc())
            .limit(limit)
            .all())
    
    return jsonify([
        {
            "id": str(tag.id),
            "name": tag.name,
            "class_count": len([c for c in tag.classes if not university_id or str(c.university_id) == university_id])
        }
        for tag in tags
    ])


# ---------- GET /tags/stats ----------
@tags_bp.route("/tags/stats", methods=["GET"])
def get_tag_stats():
    """Get overall tag statistics"""
    total_tags = Tag.query.count()
    
    # Tags with no classes
    unused_tags = Tag.query.outerjoin(Tag.classes).group_by(Tag.id).having(func.count(Class.id) == 0).count()
    
    # Most used tag
    most_used = (Tag.query.join(Tag.classes)
                 .group_by(Tag.id)
                 .order_by(func.count(Class.id).desc())
                 .first())
    
    return jsonify({
        "total_tags": total_tags,
        "unused_tags": unused_tags,
        "tags_in_use": total_tags - unused_tags,
        "most_popular_tag": {
            "id": str(most_used.id),
            "name": most_used.name,
            "class_count": len(most_used.classes)
        } if most_used else None
    })