from flask import Flask
from flask_cors import CORS
from models import db, User, Post
import os

app = Flask(__name__)
CORS(app)

# SQLite path
db_path = os.path.join(os.path.dirname(__file__), "database", "universe.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db with Flask
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

# Example test route
@app.route("/")
def home():
    return {"message": "UniVerse API is running!"}

if __name__ == "__main__":
    app.run(debug=True)
