from flask import request, abort
from flask_smorest import Blueprint
from models import db, Class, University, Tag
from schemas import ClassSchema, ClassCreateSchema, ClassUpdateSchema
from sqlalchemy import func
import uuid

# NEW: import service
from services.grouping_service import assign_class_to_group

class_bp = Blueprint("classes", __name__, url_prefix="/api/classes", description="Class operations")

# ---------- GET /classes ----------
@class_bp.route("/", methods=["GET"])
@class_bp.response(200, ClassSchema(many=True))
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
    return classes


# ---------- GET /classes/<id> ----------
@class_bp.route("/<uuid:class_id>", methods=["GET"])
@class_bp.response(200, ClassSchema)
def get_class(class_id):
    """Get details of a single class"""
    c = Class.query.get_or_404(class_id)
    return c


# ---------- POST /classes ----------
@class_bp.route("/", methods=["POST"])
@class_bp.arguments(ClassCreateSchema)
@class_bp.response(201, ClassSchema)
def create_class(data):
    """Create a new class"""
    uni = University.query.get(data["university_id"])
    if not uni:
        abort(404, description="University not found")

    existing = Class.query.filter_by(
        name=data["name"], 
        university_id=data["university_id"]
    ).first()
    print(f"Looking for class: name='{data['name']}', university_id='{data['university_id']}'")
    print(f"Found existing class: {existing}")

    if existing:
        print(f"Existing class details: id={existing.id}, name={existing.name}, university_id={existing.university_id}")
        abort(400, description="A class with this name already exists in the university")

    new_class = Class(
        id=uuid.uuid4(),
        name=data["name"],
        university_id=data["university_id"]
    )

    # Attach tags if provided
    tag_ids = data.get("tag_ids", [])
    if tag_ids:
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        new_class.tags = tags

    db.session.add(new_class)
    db.session.commit()   # ensure new_class.id exists for mapping

    # --- HERO: auto group across universities ---
    assign_class_to_group(new_class)

    # Re-load if you want fresh relationships for serialization (optional)
    return Class.query.get(new_class.id)


# ---------- PUT /classes/<id> ----------
@class_bp.route("/<uuid:class_id>", methods=["PUT"])
@class_bp.arguments(ClassUpdateSchema)
@class_bp.response(200, ClassSchema)
def update_class(data, class_id):
    """Update class name or tags"""
    c = Class.query.get_or_404(class_id)

    if "name" in data:
        existing = Class.query.filter_by(
            name=data["name"], 
            university_id=c.university_id
        ).first()
        if existing and existing.id != c.id:
            class_bp.abort(400, message="A class with this name already exists in the university")
        c.name = data["name"]

    if "tag_ids" in data:
        c.tags = Tag.query.filter(Tag.id.in_(data["tag_ids"])).all()

    db.session.commit()

    # --- HERO: re-evaluate grouping if name/tags changed ---
    assign_class_to_group(c)

    return Class.query.get(c.id)


# ---------- DELETE /classes/<id> ----------
@class_bp.route("/<uuid:class_id>", methods=["DELETE"])
@class_bp.response(204)
def delete_class(class_id):
    """Delete a class"""
    c = Class.query.get_or_404(class_id)
    db.session.delete(c)
    db.session.commit()
    return {}
