from flask import Flask
from flask_cors import CORS
from models import db, User
from sqlalchemy import event
from sqlalchemy.engine import Engine
import os
from routes.discussion import discussion_bp



app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(discussion_bp, url_prefix="/api")


# SQLite path
db_path = os.path.join(os.path.dirname(__file__), "database", "universe.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Without this, CASCADE deletes don't work
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# Initialize db with Flask
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.drop_all()
    db.create_all()

# Example test route
@app.route("/")
def home():
    return {"message": "UniVerse API is running!"}

if __name__ == "__main__":
    app.run(debug=True)
