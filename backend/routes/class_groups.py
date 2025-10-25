from flask_smorest import Blueprint
from models import Class, University
from models import ClassGroupMap
groups_bp = Blueprint("class_groups", __name__, url_prefix="/api/class-groups")

@groups_bp.route("/by-class/<uuid:class_id>", methods=["GET"])
def by_class(class_id):
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
