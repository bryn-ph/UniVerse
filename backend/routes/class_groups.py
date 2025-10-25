from flask_smorest import Blueprint
from models import db, Class, ClassGroup, ClassGroupMap
from schemas import ClassGroupSchema, ClassGroupCreateSchema, ClassGroupUpdateSchema
import uuid

class_group_bp = Blueprint("class_groups", __name__, url_prefix="/api/class-groups", description="Class group operations")

@class_group_bp.route("/", methods=["GET"])
@class_group_bp.response(200, ClassGroupSchema(many=True))
def get_class_groups():
    """Get all class groups"""
    return ClassGroup.query.all()

@class_group_bp.route("/<uuid:group_id>", methods=["GET"])
@class_group_bp.response(200, ClassGroupSchema)
def get_class_group(group_id):
    """Get a class group with all its classes"""
    return ClassGroup.query.get_or_404(group_id)

@class_group_bp.route("/", methods=["POST"])
@class_group_bp.arguments(ClassGroupCreateSchema)
@class_group_bp.response(201, ClassGroupSchema)
def create_class_group(data):
    """Create a new class group"""
    group = ClassGroup(
        id=uuid.uuid4(),
        name=data["name"],
        description=data.get("description"),
        signature=data["name"].lower().replace(" ", "-"),  # Generate signature from name
    )
    db.session.add(group)
    db.session.commit()
    return group

@class_group_bp.route("/<uuid:group_id>", methods=["PUT"])
@class_group_bp.arguments(ClassGroupUpdateSchema)
@class_group_bp.response(200, ClassGroupSchema)
def update_class_group(data, group_id):
    """Update a class group"""
    group = ClassGroup.query.get_or_404(group_id)
    if "name" in data:
        group.name = data["name"]
    if "description" in data:
        group.description = data["description"]
    db.session.commit()
    return group

@class_group_bp.route("/<uuid:group_id>", methods=["DELETE"])
@class_group_bp.response(204)
def delete_class_group(group_id):
    """Delete a class group"""
    group = ClassGroup.query.get_or_404(group_id)
    db.session.delete(group)
    db.session.commit()
    return {}

@class_group_bp.route("/by-class/<uuid:class_id>", methods=["GET"])
def by_class(class_id):
    """Get all classes in the same group as the given class"""
    mapping = ClassGroupMap.query.filter_by(class_id=class_id).first_or_404()
    siblings = ClassGroupMap.query.filter_by(group_id=mapping.group_id).all()
    ids = [m.class_id for m in siblings]
    classes = Class.query.filter(Class.id.in_(ids)).all()
    out = []
    for c in classes:
        out.append({
            "class_id": str(c.id),
            "name": c.name,
            "university": c.university.name,
            "tags": [t.name for t in c.tags],
        })
    return {"group_id": str(mapping.group_id), "classes": out}
