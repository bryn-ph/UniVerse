from flask_smorest import Blueprint
from models import db, University
from schemas import UniversitySchema, ClassSchema
import uuid

university_bp = Blueprint("university", __name__, url_prefix="/api/universities")

# ---------- GET /universities ----------
@university_bp.route("/", methods=["GET"])
@university_bp.response(200, UniversitySchema(many=True))
def get_universities():
    """List all universities"""
    q = University.query
    search = uuid.request.args.get("q")
    if search:
        q = q.filter(University.name.ilike(f"%{search}%"))
    universities = q.order_by(University.name.asc()).all()

    for u in universities:
        u.user_count = len(u.users)
        u.class_count = len(u.classes)
    return universities


# ---------- GET /universities/<id> ----------
@university_bp.route("/<uuid:university_id>", methods=["GET"])
@university_bp.response(200, UniversitySchema)
def get_university(university_id):
    """Get a specific university"""
    uni = University.query.get_or_404(university_id)
    uni.user_count = len(uni.users)
    uni.class_count = len(uni.classes)
    return uni


# ---------- POST /universities ----------
@university_bp.route("/", methods=["POST"])
@university_bp.arguments(UniversitySchema)
@university_bp.response(201, UniversitySchema)
def create_university(data):
    """Create a new university"""
    existing = University.query.filter_by(name=data["name"]).first()
    if existing:
        return {"error": "University already exists"}, 409
    uni = University(name=data["name"])
    db.session.add(uni)
    db.session.commit()
    uni.user_count = 0
    uni.class_count = 0
    return uni


# ---------- DELETE /universities/<id> ----------
@university_bp.route("/<uuid:university_id>", methods=["DELETE"])
@university_bp.response(204)
def delete_university(university_id):
    """Delete a university"""
    uni = University.query.get_or_404(university_id)
    db.session.delete(uni)
    db.session.commit()
    return {}
