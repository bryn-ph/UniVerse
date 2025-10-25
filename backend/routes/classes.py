from flask import Blueprint, request, jsonify
from models import db, Class, University, Tag
from sqlalchemy import func
import uuid

class_bp = Blueprint("class", __name__)

# ---------- GET /classes ----------
@class_bp.route("/classes", methods=["GET"])
def get_classes():
    """Get all classes (optionally filtered by university or tag)"""
    university_id = request.args.get("university_id")
    tag_id = request.args.get("tag_id")
    search = request.args.get("q")

    q = Class.query.join(Class.university)

    if university_id:
        q = q.filter(Class.university_id == university_id)
    if tag_id:
        q = q.join(Class.tags).filter(Tag.id == tag_id)
    if search:
        q = q.filter(Class.name.ilike(f"%{search}%"))

    classes = q.order_by(Class.name.asc()).all()

    return jsonify([
        {
            "id": str(c.id),
            "name": c.name,
            "university": c.university.name if c.university else None,
            "tags": [t.name for t in c.tags],
        }
        for c in classes
    ])


# ---------- GET /classes/<id> ----------
@class_bp.route("/classes/<uuid:class_id>", methods=["GET"])
def get_class(class_id):
    """Get details of a single class"""
    c = Class.query.get(class_id)
    if not c:
        return jsonify({"error": "Class not found"}), 404

    return jsonify({
        "id": str(c.id),
        "name": c.name,
        "university": c.university.name if c.university else None,
        "university_id": str(c.university_id),
        "tags": [t.name for t in c.tags],
    })


# ---------- POST /classes ----------
@class_bp.route("/classes", methods=["POST"])
def create_class():
    """Create a new class"""
    data = request.get_json()
    name = data.get("name")
    university_id = data.get("university_id")
    tag_ids = data.get("tag_ids", [])

    if not all([name, university_id]):
        return jsonify({"error": "Missing required fields"}), 400

    uni = University.query.get(university_id)
    if not uni:
        return jsonify({"error": "Invalid university_id"}), 404

    # Check unique constraint (name per university)
    existing = Class.query.filter_by(name=name, university_id=university_id).first()
    if existing:
        return jsonify({"error": "A class with this name already exists in the university"}), 400

    new_class = Class(
        id=uuid.uuid4(),
        name=name,
        university_id=university_id
    )

    # Attach tags if provided
    if tag_ids:
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        new_class.tags = tags

    db.session.add(new_class)
    db.session.commit()

    return jsonify({
        "message": "Class created successfully",
        "class": {
            "id": str(new_class.id),
            "name": new_class.name,
            "university": new_class.university.name,
            "tags": [t.name for t in new_class.tags],
        }
    }), 201


# ---------- PUT /classes/<id> ----------
@class_bp.route("/classes/<uuid:class_id>", methods=["PUT"])
def update_class(class_id):
    """Update class name or tags"""
    c = Class.query.get(class_id)
    if not c:
        return jsonify({"error": "Class not found"}), 404

    data = request.get_json()
    name = data.get("name")
    tag_ids = data.get("tag_ids")

    if name:
        # Ensure uniqueness within same university
        existing = Class.query.filter_by(name=name, university_id=c.university_id).first()
        if existing and existing.id != c.id:
            return jsonify({"error": "A class with this name already exists in the university"}), 400
        c.name = name

    if tag_ids is not None:
        c.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.commit()

    return jsonify({"message": "Class updated successfully"})


# ---------- DELETE /classes/<id> ----------
@class_bp.route("/classes/<uuid:class_id>", methods=["DELETE"])
def delete_class(class_id):
    """Delete a class"""
    c = Class.query.get(class_id)
    if not c:
        return jsonify({"error": "Class not found"}), 404

    db.session.delete(c)
    db.session.commit()
    return jsonify({"message": "Class deleted successfully"})
