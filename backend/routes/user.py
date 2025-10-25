from flask import Blueprint, request, jsonify
from models import db, User, University
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
import uuid

user_bp = Blueprint("user", __name__)

# ---------- GET /users ----------
@user_bp.route("/users", methods=["GET"])
def get_users():
    """Get all users (optionally filtered by university_id or search query)"""
    university_id = request.args.get("university_id")
    search = request.args.get("q")

    q = User.query.join(User.university)
    if university_id:
        q = q.filter(User.university_id == university_id)
    if search:
        q = q.filter(User.name.ilike(f"%{search}%"))

    users = q.order_by(User.created_at.desc()).all()

    return jsonify([
        {
            "id": str(u.id),
            "name": u.name,
            "email": u.email,
            "university": u.university.name if u.university else None,
            "created_at": u.created_at.isoformat(),
        }
        for u in users
    ])


# ---------- GET /users/<id> ----------
@user_bp.route("/users/<uuid:user_id>", methods=["GET"])
def get_user(user_id):
    """Get a specific user by ID"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": str(user.id),
        "name": user.name,
        "email": user.email,
        "university": user.university.name if user.university else None,
        "created_at": user.created_at.isoformat(),
    })


# ---------- POST /users ----------
@user_bp.route("/users", methods=["POST"])
def create_user():
    """Create a new user"""
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    university_id = data.get("university_id")

    if not all([name, email, password, university_id]):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    uni = University.query.get(university_id)
    if not uni:
        return jsonify({"error": "Invalid university_id"}), 404

    hashed_pw = generate_password_hash(password)
    new_user = User(
        id=uuid.uuid4(),
        name=name,
        email=email,
        password=hashed_pw,
        university_id=university_id,
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User created successfully",
        "user": {
            "id": str(new_user.id),
            "name": new_user.name,
            "email": new_user.email,
            "university": new_user.university.name,
            "created_at": new_user.created_at.isoformat(),
        }
    }), 201


# ---------- PUT /users/<id> ----------
@user_bp.route("/users/<uuid:user_id>", methods=["PUT"])
def update_user(user_id):
    """Update user details"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    name = data.get("name")
    password = data.get("password")

    if name:
        user.name = name
    if password:
        user.password = generate_password_hash(password)

    db.session.commit()
    return jsonify({"message": "User updated successfully"})


# ---------- DELETE /users/<id> ----------
@user_bp.route("/users/<uuid:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Delete a user"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})


# ---------- POST /users/login ----------
@user_bp.route("/users/login", methods=["POST"])
def login_user():
    """Simple login endpoint"""
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not all([email, password]):
        return jsonify({"error": "Missing credentials"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 401

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "university": user.university.name if user.university else None,
        }
    })
