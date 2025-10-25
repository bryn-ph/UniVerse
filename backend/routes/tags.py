from flask import request, jsonify, abort
from flask_smorest import Blueprint
from models import db, Tag, Class
from schemas import TagSchema, TagCreateSchema, TagUpdateSchema
from sqlalchemy import func
import uuid

tags_bp = Blueprint("tags", __name__, url_prefix="/api/tags", description="Tag operations")

# ---------- GET /tags ----------
@tags_bp.route("/", methods=["GET"])
@tags_bp.response(200, TagSchema(many=True))
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
    return tags


# ---------- GET /tags/<tag_id> ----------
@tags_bp.route("/<uuid:tag_id>", methods=["GET"])
@tags_bp.response(200, TagSchema)
def get_tag(tag_id):
    """Get a specific tag with all its associated classes"""
    tag = Tag.query.get_or_404(tag_id)
    return tag


# ---------- POST /tags ----------
@tags_bp.route("/", methods=["POST"])
@tags_bp.arguments(TagCreateSchema)
@tags_bp.response(201, TagSchema)
def create_tag(data):
    """Create a new tag"""
    # Check if tag already exists (case-insensitive)
    existing_tag = Tag.query.filter(
        func.lower(Tag.name) == func.lower(data["name"])
    ).first()
    if existing_tag:
        abort(409, description="Tag already exists")
    
    # Create new tag
    new_tag = Tag(name=data["name"].strip())
    db.session.add(new_tag)
    db.session.commit()
    return new_tag


# ---------- PUT /tags/<tag_id> ----------
@tags_bp.route("/<uuid:tag_id>", methods=["PUT"])
@tags_bp.arguments(TagUpdateSchema)
@tags_bp.response(200, TagSchema)
def update_tag(data, tag_id):
    """Update a tag's name"""
    tag = Tag.query.get_or_404(tag_id)
    
    # Check if new name already exists (excluding current tag)
    existing_tag = Tag.query.filter(
        func.lower(Tag.name) == func.lower(data["name"]),
        Tag.id != tag_id
    ).first()
    
    if existing_tag:
        abort(409, description="A tag with this name already exists")
    
    tag.name = data["name"].strip()
    db.session.commit()
    return tag


# ---------- DELETE /tags/<tag_id> ----------
@tags_bp.route("/<uuid:tag_id>", methods=["DELETE"])
@tags_bp.response(204)
def delete_tag(tag_id):
    """Delete a tag (this will also remove it from all associated classes)"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return {}


# ---------- GET /tags/<tag_id>/classes ----------
@tags_bp.route("/<uuid:tag_id>/classes", methods=["GET"])
def get_tag_classes(tag_id):
    """Get all classes associated with a specific tag"""
    tag = Tag.query.get_or_404(tag_id)
    
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
                "tags": [{"id": str(t.id), "name": t.name} for t in c.tags]
            }
            for c in classes
        ],
        "total_classes": len(classes)
    })


# ---------- GET /tags/popular ----------
@tags_bp.route("/popular", methods=["GET"])
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
@tags_bp.route("/stats", methods=["GET"])
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