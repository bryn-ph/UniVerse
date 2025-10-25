from flask import Flask
from flask_cors import CORS
from models import db, User
from sqlalchemy import event
from sqlalchemy.engine import Engine
import os
from routes.discussion import discussion_bp
from routes.tags import tags_bp
from routes.reply import reply_bp
from routes.university import university_bp
from routes.user import user_bp
from routes.classes import class_bp
from flask_smorest import Api
from marshmallow import ValidationError
from flask import jsonify


app = Flask(__name__)
CORS(app)

# Database config - MUST be set BEFORE db.init_app()
db_path = os.path.join(os.path.dirname(__file__), "database", "universe.db")
os.makedirs(os.path.dirname(db_path), exist_ok=True)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Smorest / OpenAPI config
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

# Register blueprints
api = Api(app)
api.register_blueprint(user_bp)
api.register_blueprint(university_bp)
api.register_blueprint(discussion_bp)
api.register_blueprint(reply_bp)
api.register_blueprint(class_bp)
api.register_blueprint(tags_bp)

# Without this, CASCADE deletes don't work
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# Create tables if they don't exist
with app.app_context():
    db.create_all()

# Example test route
@app.route("/")
def home():
    return {"message": "UniVerse API is running!"}

if __name__ == "__main__":
    app.run(debug=True, port=5001)
