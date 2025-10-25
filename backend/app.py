from flask import Flask, jsonify
from flask_cors import CORS
from models import db
from sqlalchemy import event
from sqlalchemy.engine import Engine
import os

# Import blueprints
from routes.discussion import discussion_bp
from routes.tags import tags_bp
from routes.reply import reply_bp
from routes.university import university_bp
from routes.user import user_bp
from routes.classes import class_bp

from flask_smorest import Api

app = Flask(__name__)
CORS(app)

# SQLite path - Define ONCE at the top
db_path = os.path.join(os.path.dirname(__file__), "database", "universe.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Flask-Smorest / OpenAPI config
app.config["API_TITLE"] = "UniVerse API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_JSON_PATH"] = "openapi.json"
app.config["OPENAPI_REDOC_PATH"] = "/redoc"
app.config["OPENAPI_REDOC_URL"] = "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

# Initialize db with Flask
db.init_app(app)

# Without this, CASCADE deletes don't work in SQLite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# Create tables if they don't exist
with app.app_context():
    db.create_all()
    print("✅ Database tables created!")

# Initialize Flask-Smorest API
api = Api(app)

# Register blueprints
api.register_blueprint(user_bp)
api.register_blueprint(university_bp)
api.register_blueprint(discussion_bp)
api.register_blueprint(reply_bp)
app.register_blueprint(tags_bp, url_prefix="/api")
app.register_blueprint(class_bp, url_prefix="/api")

# Root route
@app.route("/")
def home():
    return jsonify({"message": "UniVerse API is running!", "status": "ok"})

# API info route
@app.route("/api")
def api_info():
    return jsonify({
        "message": "UniVerse API",
        "version": "1.0",
        "documentation": {
            "swagger": "/swagger",
            "redoc": "/redoc"
        },
        "endpoints": {
            "users": "/users",
            "universities": "/universities",
            "discussions": "/discussions",
            "replies": "/replies",
            "tags": "/api/tags",
            "classes": "/api/classes"
        }
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found", "status": 404}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error", "status": 500}), 500

if __name__ == "__main__":
    app.run(debug=True)
