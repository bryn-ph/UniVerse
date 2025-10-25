from flask_smorest import Blueprint
from flask import request
from models import db, User, University, Class
from schemas import UserBaseSchema, UserCreateSchema, UserLoginSchema, UserUpdateSchema, UserEnrollSchema, UserEnrollBulkSchema, ClassSchema
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

user_bp = Blueprint("user", __name__, url_prefix="/api/users")

# ---------- GET /users ----------
@user_bp.route("/", methods=["GET"])
@user_bp.response(200, UserBaseSchema(many=True))
def get_users():
    """List all users (optionally filtered by university or search query)"""
    university_id = request.args.get("university_id")
    search = request.args.get("q")

    q = User.query.join(User.university)
    if university_id:
        q = q.filter(User.university_id == university_id)
    if search:
        q = q.filter(User.name.ilike(f"%{search}%"))

    return q.order_by(User.created_at.desc()).all()


# ---------- GET /users/<id> ----------
@user_bp.route("/<uuid:user_id>", methods=["GET"])
@user_bp.response(200, UserBaseSchema)
def get_user(user_id):
    """Get a single user"""
    return User.query.get_or_404(user_id)


# ---------- POST /users ----------
@user_bp.route("/", methods=["POST"])
@user_bp.arguments(UserCreateSchema)
@user_bp.response(201, UserBaseSchema)
def create_user(data):
    """Create a new user"""
    if User.query.filter_by(email=data["email"]).first():
        return {"error": "Email already registered"}, 400

    if not University.query.get(data["university_id"]):
        return {"error": "Invalid university_id"}, 404

    user = User(
        id=uuid.uuid4(),
        name=data["name"],
        email=data["email"],
        password=generate_password_hash(data["password"]),
        university_id=data["university_id"],
    )
    db.session.add(user)
    db.session.commit()
    return user


# ---------- PUT /users/<id> ----------
@user_bp.route("/<uuid:user_id>", methods=["PUT"])
@user_bp.arguments(UserUpdateSchema)
@user_bp.response(200, UserBaseSchema)
def update_user(data, user_id):
    """Update user details"""
    user = User.query.get_or_404(user_id)
    if "name" in data:
        user.name = data["name"]
    if "password" in data:
        user.password = generate_password_hash(data["password"])
    db.session.commit()
    return user


# ---------- DELETE /users/<id> ----------
@user_bp.route("/<uuid:user_id>", methods=["DELETE"])
@user_bp.response(204)
def delete_user(user_id):
    """Delete a user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return {}


# ---------- POST /users/login ----------
@user_bp.route("/login", methods=["POST"])
@user_bp.arguments(UserLoginSchema)
@user_bp.response(200)
def login_user(data):
    """Simple login endpoint"""
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not check_password_hash(user.password, data["password"]):
        return {"error": "Invalid email or password"}, 401
    return {
        "message": "Login successful",
        "user": {
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "university": user.university.name if user.university else None,
            "university_id": str(user.university_id) if user.university_id else None,
        },
    }


# ---------- GET /users/<id>/classes ----------
@user_bp.route("/<uuid:user_id>/classes", methods=["GET"])
@user_bp.response(200, ClassSchema(many=True))
def get_user_classes(user_id):
    """Get all classes user is enrolled in"""
    user = User.query.get_or_404(user_id)
    return user.classes


# ---------- POST /users/<id>/classes ----------
@user_bp.route("/<uuid:user_id>/classes", methods=["POST"])
@user_bp.arguments(UserEnrollSchema)
@user_bp.response(201, ClassSchema)
def enroll_in_class(data, user_id):
    """Enroll user in a class"""
    user = User.query.get_or_404(user_id)
    class_obj = Class.query.get_or_404(data["class_id"])

    # Check if already enrolled
    if class_obj in user.classes:
        return {"error": "Already enrolled in this class"}, 400

    # Check if class belongs to user's university
    if class_obj.university_id != user.university_id:
        return {"error": "Can only enroll in classes from your university"}, 400

    user.classes.append(class_obj)
    db.session.commit()
    return class_obj


# ---------- DELETE /users/<id>/classes/<class_id> ----------
@user_bp.route("/<uuid:user_id>/classes/<uuid:class_id>", methods=["DELETE"])
@user_bp.response(204)
def unenroll_from_class(user_id, class_id):
    """Unenroll user from a class"""
    user = User.query.get_or_404(user_id)
    class_obj = Class.query.get_or_404(class_id)

    if class_obj not in user.classes:
        return {"error": "Not enrolled in this class"}, 400

    user.classes.remove(class_obj)
    db.session.commit()
    return {}


# ---------- PUT /users/<id>/classes ----------
@user_bp.route("/<uuid:user_id>/classes", methods=["PUT"])
@user_bp.arguments(UserEnrollBulkSchema)
@user_bp.response(200, ClassSchema(many=True))
def update_user_classes(data, user_id):
    """Bulk update user's enrolled classes"""
    user = User.query.get_or_404(user_id)

    # Get all classes by IDs
    class_ids = data["class_ids"]
    classes = Class.query.filter(Class.id.in_(class_ids)).all()

    # Validate all classes belong to user's university
    for class_obj in classes:
        if class_obj.university_id != user.university_id:
            return {"error": f"Class '{class_obj.name}' is not from your university"}, 400

    # Replace all enrolled classes
    user.classes = classes
    db.session.commit()
    return user.classes
