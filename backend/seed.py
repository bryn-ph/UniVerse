import os
from app import app, db
from models import User, University, Class, Tag, Discussion, Reply
from werkzeug.security import generate_password_hash

def ensure_database_folder():
    """Ensure the database folder exists"""
    db_folder = os.path.join(os.path.dirname(__file__), "database")
    
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)
        print(f"✅ Created database folder at: {db_folder}")
    else:
        print(f"✅ Database folder exists at: {db_folder}")
    
    return db_folder

def clear_data():
    """Clear all existing data and recreate tables"""
    print("\n" + "="*60)
    print("CLEARING EXISTING DATA")
    print("="*60)
    
    with app.app_context():
        db.drop_all()
        print("✅ Dropped all tables")
        
        db.create_all()
        print("✅ Created all tables")
    
    print("="*60)

def seed_data():
    """Seed the database with sample data"""
    print("\n" + "="*60)
    print("SEEDING DATABASE")
    print("="*60)
    
    with app.app_context():
        # Create Universities
        print("\n📚 Creating universities...")
        uni1 = University(name="Stanford University")
        uni2 = University(name="MIT")
        uni3 = University(name="UC Berkeley")
        
        db.session.add_all([uni1, uni2, uni3])
        db.session.commit()
        print(f"   ✅ Created {University.query.count()} universities")
        
        # Create Users
        print("\n👥 Creating users...")
        users = [
            User(name="Alice Johnson", email="alice@stanford.edu", password=generate_password_hash("password123"), university_id=uni1.id),
            User(name="Bob Smith", email="bob@stanford.edu", password=generate_password_hash("password123"), university_id=uni1.id),
            User(name="Charlie Brown", email="charlie@mit.edu", password=generate_password_hash("password123"), university_id=uni2.id),
            User(name="Diana Prince", email="diana@mit.edu", password=generate_password_hash("password123"), university_id=uni2.id),
            User(name="Eve Martinez", email="eve@berkeley.edu", password=generate_password_hash("password123"), university_id=uni3.id),
            User(name="Frank Zhang", email="frank@berkeley.edu", password=generate_password_hash("password123"), university_id=uni3.id),
            User(name="Grace Lee", email="grace@stanford.edu", password=generate_password_hash("password123"), university_id=uni1.id),
            User(name="Henry Wilson", email="henry@mit.edu", password=generate_password_hash("password123"), university_id=uni2.id),
        ]
        
        db.session.add_all(users)
        db.session.commit()
        print(f"   ✅ Created {User.query.count()} users")
        
        # Create Tags
        print("\n🏷️  Creating tags...")
        tags = [
            Tag(name="Computer Science"),
            Tag(name="Mathematics"),
            Tag(name="Physics"),
            Tag(name="Engineering"),
            Tag(name="Biology"),
            Tag(name="Chemistry"),
            Tag(name="Economics"),
            Tag(name="Statistics"),
            Tag(name="Machine Learning"),
            Tag(name="Data Science"),
        ]
        
        db.session.add_all(tags)
        db.session.commit()
        print(f"   ✅ Created {Tag.query.count()} tags")
        
        # Create Classes
        print("\n📖 Creating classes...")
        
        # Stanford Classes
        cs101 = Class(name="Introduction to Computer Science", university_id=uni1.id)
        cs101.tags.extend([tags[0], tags[1]])  # CS, Math
        
        cs229 = Class(name="Machine Learning", university_id=uni1.id)
        cs229.tags.extend([tags[0], tags[8], tags[9]])  # CS, ML, Data Science
        
        math51 = Class(name="Linear Algebra", university_id=uni1.id)
        math51.tags.extend([tags[1], tags[7]])  # Math, Statistics
        
        # MIT Classes
        mit_cs = Class(name="Algorithms and Data Structures", university_id=uni2.id)
        mit_cs.tags.extend([tags[0], tags[1]])
        
        mit_ai = Class(name="Artificial Intelligence", university_id=uni2.id)
        mit_ai.tags.extend([tags[0], tags[8]])
        
        # Berkeley Classes
        berkeley_ds = Class(name="Data Science Fundamentals", university_id=uni3.id)
        berkeley_ds.tags.extend([tags[0], tags[7], tags[9]])
        
        berkeley_physics = Class(name="Quantum Mechanics", university_id=uni3.id)
        berkeley_physics.tags.extend([tags[2], tags[1]])
        
        all_classes = [cs101, cs229, math51, mit_cs, mit_ai, berkeley_ds, berkeley_physics]
        db.session.add_all(all_classes)
        db.session.commit()
        print(f"   ✅ Created {Class.query.count()} classes")
        
        # Create Discussions
        print("\n💬 Creating discussions...")
        discussions = [
            # CS101 discussions
            Discussion(
                title="How do I install Python?",
                body="I'm having trouble installing Python on my Mac. Can anyone help?",
                user_id=users[0].id,
                class_id=cs101.id
            ),
            Discussion(
                title="Understanding recursion",
                body="Can someone explain how recursion works? The factorial example in lecture was confusing.",
                user_id=users[1].id,
                class_id=cs101.id
            ),
            
            # CS229 discussions
            Discussion(
                title="Gradient descent not converging",
                body="My gradient descent implementation doesn't seem to converge. Here's my code...",
                user_id=users[6].id,
                class_id=cs229.id
            ),
            Discussion(
                title="Best resources for understanding neural networks?",
                body="Looking for good supplementary materials to understand backpropagation better.",
                user_id=users[0].id,
                class_id=cs229.id
            ),
            
            # MIT AI discussions
            Discussion(
                title="Midterm study group?",
                body="Anyone want to form a study group for the upcoming midterm?",
                user_id=users[2].id,
                class_id=mit_ai.id
            ),
            Discussion(
                title="A* search algorithm question",
                body="I don't understand why A* is optimal. Can someone explain?",
                user_id=users[3].id,
                class_id=mit_ai.id
            ),
            
            # Berkeley Data Science discussions
            Discussion(
                title="Project partners needed",
                body="Looking for 2 people to join my project team. DM me if interested!",
                user_id=users[4].id,
                class_id=berkeley_ds.id
            ),
            Discussion(
                title="Pandas vs NumPy - when to use which?",
                body="I'm confused about when I should use Pandas DataFrames vs NumPy arrays.",
                user_id=users[5].id,
                class_id=berkeley_ds.id
            ),
        ]
        
        db.session.add_all(discussions)
        db.session.commit()
        print(f"   ✅ Created {Discussion.query.count()} discussions")
        
        # Create Replies
        print("\n💭 Creating replies...")
        replies = [
            # Replies to "How do I install Python?"
            Reply(
                body="Go to python.org and download the latest version. The installer should work on Mac.",
                user_id=users[1].id,
                discussion_id=discussions[0].id
            ),
            Reply(
                body="I recommend using Homebrew! Just run: brew install python",
                user_id=users[6].id,
                discussion_id=discussions[0].id
            ),
            Reply(
                body="Thanks both! The Homebrew method worked perfectly.",
                user_id=users[0].id,
                discussion_id=discussions[0].id
            ),
            
            # Replies to "Understanding recursion"
            Reply(
                body="Think of it like this: a function that calls itself until it reaches a base case.",
                user_id=users[0].id,
                discussion_id=discussions[1].id
            ),
            Reply(
                body="This video helped me: [link]. The visualization really made it click.",
                user_id=users[6].id,
                discussion_id=discussions[1].id
            ),
            
            # Replies to "Gradient descent not converging"
            Reply(
                body="Try reducing your learning rate. It might be overshooting.",
                user_id=users[0].id,
                discussion_id=discussions[2].id
            ),
            Reply(
                body="Also make sure you're normalizing your features!",
                user_id=users[1].id,
                discussion_id=discussions[2].id
            ),
            
            # Replies to "Best resources for understanding neural networks?"
            Reply(
                body="3Blue1Brown has an amazing series on neural networks on YouTube.",
                user_id=users[1].id,
                discussion_id=discussions[3].id
            ),
            Reply(
                body="The Deep Learning book by Goodfellow is great if you want something more rigorous.",
                user_id=users[6].id,
                discussion_id=discussions[3].id
            ),
            
            # Replies to "Midterm study group?"
            Reply(
                body="I'm in! When and where?",
                user_id=users[3].id,
                discussion_id=discussions[4].id
            ),
            Reply(
                body="Count me in too. How about Saturday at the library?",
                user_id=users[7].id,
                discussion_id=discussions[4].id
            ),
            
            # Replies to "A* search algorithm question"
            Reply(
                body="A* is optimal when the heuristic is admissible (never overestimates).",
                user_id=users[2].id,
                discussion_id=discussions[5].id
            ),
            
            # Replies to "Project partners needed"
            Reply(
                body="What's the project about?",
                user_id=users[5].id,
                discussion_id=discussions[6].id
            ),
            Reply(
                body="I'm interested! I have experience with machine learning.",
                user_id=users[4].id,
                discussion_id=discussions[6].id
            ),
            
            # Replies to "Pandas vs NumPy"
            Reply(
                body="Use Pandas when working with tabular data (like CSV files). Use NumPy for numerical computations.",
                user_id=users[4].id,
                discussion_id=discussions[7].id
            ),
            Reply(
                body="Pandas is built on top of NumPy, so they work well together!",
                user_id=users[5].id,
                discussion_id=discussions[7].id
            ),
        ]
        
        db.session.add_all(replies)
        db.session.commit()
        print(f"   ✅ Created {Reply.query.count()} replies")
        
        # Summary
        print("\n" + "="*60)
        print("✅ DATABASE SEEDED SUCCESSFULLY!")
        print("="*60)
        print("\n📊 Summary:")
        print(f"   • {University.query.count()} universities")
        print(f"   • {User.query.count()} users")
        print(f"   • {Tag.query.count()} tags")
        print(f"   • {Class.query.count()} classes")
        print(f"   • {Discussion.query.count()} discussions")
        print(f"   • {Reply.query.count()} replies")
        print("="*60 + "\n")

def check_database_location():
    """Show where the database file is located"""
    db_folder = os.path.join(os.path.dirname(__file__), "database")
    db_file = os.path.join(db_folder, "universe.db")
    
    print("\n" + "="*60)
    print("DATABASE INFORMATION")
    print("="*60)
    print(f"📁 Database folder: {db_folder}")
    print(f"📄 Database file: {db_file}")
    
    if os.path.exists(db_file):
        file_size = os.path.getsize(db_file)
        print(f"💾 File size: {file_size:,} bytes ({file_size/1024:.2f} KB)")
        print("✅ Database file exists")
    else:
        print("⚠️  Database file does not exist yet")
    print("="*60)

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🌌 UNIVERSE DATABASE SEEDER 🌌")
    print("="*60)
    
    # Ensure database folder exists
    db_folder = ensure_database_folder()
    
    # Show current database location
    check_database_location()
    
    # Ask for confirmation
    print("\n⚠️  WARNING: This will clear all existing data!")
    response = input("Continue? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        clear_data()
        seed_data()
        check_database_location()
        
        print("\n🎉 All done! Your database is ready to use.")
        print("💡 Start your server with: python app.py")
        print("📚 View API docs at: http://localhost:5000/swagger\n")
    else:
        print("\n❌ Seeding cancelled. No changes made.\n")