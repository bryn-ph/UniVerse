from flask_smorest import Blueprint
from flask import request
from models import db, University
from schemas import UniversitySchema, ClassSchema
import uuid

university_bp = Blueprint("university", __name__, url_prefix="/api/universities")

# ---------- GET /universities ----------
@university_bp.route("/", methods=["GET"])
@university_bp.response(200, UniversitySchema(many=True))
def get_universities():
    """List all universities"""
    search = request.args.get("q")
    q = University.query
    if search:
        q = q.filter(University.name.ilike(f"%{search}%"))
    return q.order_by(University.name.asc()).all()


# ---------- GET /universities/<id> ----------
@university_bp.route("/<uuid:university_id>", methods=["GET"])
@university_bp.response(200, UniversitySchema)
def get_university(university_id):
    """Get a university by ID"""
    return University.query.get_or_404(university_id)


# ---------- POST /universities ----------
@university_bp.route("/", methods=["POST"])
@university_bp.arguments(UniversitySchema)
@university_bp.response(201, UniversitySchema)
def create_university(data):
    """Create a new university"""
    if University.query.filter_by(name=data["name"]).first():
        return {"error": "University already exists"}, 409

    uni = University(name=data["name"])
    db.session.add(uni)
    db.session.commit()
    return uni


# ---------- PUT /universities/<id> ----------
@university_bp.route("/<uuid:university_id>", methods=["PUT"])
@university_bp.arguments(UniversitySchema)
@university_bp.response(200, UniversitySchema)
def update_university(data, university_id):
    """Update a university"""
    uni = University.query.get_or_404(university_id)
    if "name" in data:
        existing = University.query.filter(
            University.name == data["name"],
            University.id != university_id
        ).first()
        if existing:
            return {"error": "Name already in use"}, 409
        uni.name = data["name"]
    db.session.commit()
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
