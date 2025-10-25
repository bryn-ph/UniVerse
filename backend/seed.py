import os
from app import app, db
from models import User, University, Class, Tag, Discussion, Reply
from services.grouping_service import assign_class_to_group
from models import ClassGroup, ClassGroupMap
from werkzeug.security import generate_password_hash

def ensure_database_folder():
    """Ensure the database folder exists"""
    db_folder = os.path.join(os.path.dirname(__file__), "database")
    
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)
        print(f" Created database folder at: {db_folder}")
    else:
        print(f" Database folder exists at: {db_folder}")
    
    return db_folder

def clear_data():
    """Clear all existing data and recreate tables"""
    print("\n" + "="*60)
    print("CLEARING EXISTING DATA")
    print("="*60)
    
    with app.app_context():
        db.drop_all()
        print("Dropped all tables")
        
        db.create_all()
        print("Created all tables")
    
    print("="*60)



def seed_data():
    """Seed the database with sample data"""
    print("\n" + "="*60)
    print("SEEDING DATABASE")
    print("="*60)
    with app.app_context():
        # Create Universities
        print("\n Creating universities...")
        uni1 = University(name="University of Melbourne")
        uni2 = University(name="UNSW Sydney")
        uni3 = University(name="Australian National University")
        uni4 = University(name="RMIT University")

        db.session.add_all([uni1, uni2, uni3, uni4])
        db.session.commit()
        print(f"Created {University.query.count()} universities")

        # ---------- Users ----------
        print("Creating users...")
        pw = generate_password_hash("password123")  # optional hashing
        users = [
            User(name="Alice Johnson", email="alice@unimelb.edu.au", password=generate_password_hash("password123"), university_id=uni1.id),
            User(name="Bob Smith", email="bob@unimelb.edu.au", password=generate_password_hash("password123"), university_id=uni1.id),
            User(name="Charlie Brown", email="charlie@unsw.edu.au", password=generate_password_hash("password123"), university_id=uni2.id),
            User(name="Diana Prince", email="diana@unsw.edu.au", password=generate_password_hash("password123"), university_id=uni2.id),
            User(name="Eve Martinez", email="eve@anu.edu.au", password=generate_password_hash("password123"), university_id=uni3.id),
            User(name="Frank Zhang", email="frank@anu.edu.au", password=generate_password_hash("password123"), university_id=uni3.id),
            User(name="Grace Lee", email="grace@unimelb.edu.au", password=generate_password_hash("password123"), university_id=uni1.id),
            User(name="Henry Wilson", email="henry@unsw.edu.au", password=generate_password_hash("password123"), university_id=uni2.id),
            User(name="Isla Walker", email="isla@rmit.edu.au", password=generate_password_hash("password123"), university_id=uni4.id),
            User(name="Jack Nguyen", email="jack@rmit.edu.au", password=generate_password_hash("password123"), university_id=uni4.id),
        ]
        db.session.add_all(users)
        db.session.commit()
        print(f"Created {User.query.count()} users")

        # ---------- Tags ----------
        print("Creating tags...")
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
        print(f"Created {Tag.query.count()} tags")

        # ---------- Classes ----------
        print("Creating classes...")

        # University of Melbourne
        cs101 = Class(name="Introduction to Computer Science", university_id=uni1.id)
        cs101.tags.extend([tags[0], tags[1]])  # CS, Math

        cs229 = Class(name="Machine Learning", university_id=uni1.id)
        cs229.tags.extend([tags[0], tags[8], tags[9]])  # CS, ML, Data Science

        math51 = Class(name="Linear Algebra", university_id=uni1.id)
        math51.tags.extend([tags[1], tags[7]])  # Math, Statistics

        # extra classes for UniMelb
        melb_se = Class(name="Software Engineering", university_id=uni1.id)
        melb_se.tags.extend([tags[0], tags[3]])
        melb_db = Class(name="Intro to Databases", university_id=uni1.id)
        melb_db.tags.extend([tags[0], tags[9]])

        # UNSW Sydney
        mit_cs = Class(name="Algorithms and Data Structures", university_id=uni2.id)
        mit_cs.tags.extend([tags[0], tags[1]])

        mit_ai = Class(name="Artificial Intelligence", university_id=uni2.id)
        mit_ai.tags.extend([tags[0], tags[8]])

        # extra classes for UNSW
        unsw_robotics = Class(name="Robotics", university_id=uni2.id)
        unsw_robotics.tags.extend([tags[3], tags[0]])
        unsw_networks = Class(name="Computer Networks", university_id=uni2.id)
        unsw_networks.tags.extend([tags[0]])

        # Australian National University
        anu_ds = Class(name="Data Science Fundamentals", university_id=uni3.id)
        anu_ds.tags.extend([tags[0], tags[7], tags[9]])

        anu_physics = Class(name="Quantum Mechanics", university_id=uni3.id)
        anu_physics.tags.extend([tags[2], tags[1]])

        # extra classes for ANU
        anu_stats = Class(name="Statistical Methods", university_id=uni3.id)
        anu_stats.tags.extend([tags[7], tags[1]])
        anu_qc = Class(name="Quantum Computing", university_id=uni3.id)
        anu_qc.tags.extend([tags[2], tags[0]])

        # RMIT
        rmit_is = Class(name="Information Systems", university_id=uni4.id)
        rmit_is.tags.extend([tags[0], tags[6]])
        rmit_cyber = Class(name="Cyber Security", university_id=uni4.id)
        rmit_cyber.tags.extend([tags[0], tags[3]])

        all_classes = [
            cs101, cs229, math51, melb_se, melb_db,
            mit_cs, mit_ai, unsw_robotics, unsw_networks,
            anu_ds, anu_physics, anu_stats, anu_qc,
            rmit_is, rmit_cyber,
        ]
        db.session.add_all(all_classes)
        db.session.commit()
        print(f"Created {Class.query.count()} classes")

        # ---------- HERO: Group classes across universities ----------
        print("Assigning classes to cross-university groups…")
        for c in Class.query.all():
            assign_class_to_group(c)
        print(f"Groups created: {ClassGroup.query.count()}")

        # ---------- Discussions ----------
        print("Creating discussions...")
        discussions = [
            Discussion(
                title="How do I install Python?",
                body="I'm having trouble installing Python on my computer. Can anyone help?",
                user_id=users[0].id,
                class_id=cs101.id
            ),
            Discussion(
                title="Understanding recursion",
                body="Can someone explain how recursion works? The factorial example in lecture was confusing.",
                user_id=users[1].id,
                class_id=cs101.id
            ),
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
            Discussion(
                title="Study group for the upcoming assessment",
                body="Anyone want to form a study group for the upcoming assessment?",
                user_id=users[2].id,
                class_id=mit_ai.id
            ),
            Discussion(
                title="A* search algorithm question",
                body="I don't understand why A* is optimal. Can someone explain?",
                user_id=users[3].id,
                class_id=mit_ai.id
            ),
            Discussion(
                title="Project partners needed",
                body="Looking for 2 people to join my project team. DM me if interested!",
                user_id=users[4].id,
                class_id=anu_ds.id
            ),
            Discussion(
                title="Pandas vs NumPy - when to use which?",
                body="I'm confused about when I should use Pandas DataFrames vs NumPy arrays.",
                user_id=users[5].id,
                class_id=anu_ds.id
            ),
            # Discussions for RMIT classes
            Discussion(
                title="Best tools for building secure web apps",
                body="Any suggestions for libraries or tools to help with secure authentication and session management?",
                user_id=users[8].id,
                class_id=rmit_cyber.id
            ),
            Discussion(
                title="How to manage company data in Information Systems",
                body="Looking for best practices when designing information systems for small businesses.",
                user_id=users[9].id,
                class_id=rmit_is.id
            ),
        ]
        db.session.add_all(discussions)
        db.session.commit()
        print(f"Created {Discussion.query.count()} discussions")

        # ---------- Replies ----------
        print("Creating replies...")
        replies = [
            Reply(
                body="Go to python.org and download the latest version. The installer should work on most platforms.",
                user_id=users[1].id,
                discussion_id=discussions[0].id
            ),
            Reply(
                body="I recommend using Homebrew on macOS or your distro's package manager on Linux.",
                user_id=users[6].id,
                discussion_id=discussions[0].id
            ),
            Reply(
                body="Thanks both! The package manager method worked perfectly.",
                user_id=users[0].id,
                discussion_id=discussions[0].id
            ),
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
            Reply(
                body="A* is optimal when the heuristic is admissible (never overestimates).",
                user_id=users[2].id,
                discussion_id=discussions[5].id
            ),
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
            # Replies for RMIT discussions
            Reply(
                body="For secure web apps look at OAuth libraries and keep sessions short. Helmet/middleware can help too.",
                user_id=users[8].id,
                discussion_id=discussions[8].id
            ),
            Reply(
                body="For small businesses, use normalized schemas and keep backups. Consider cloud-hosted DBs for reliability.",
                user_id=users[9].id,
                discussion_id=discussions[9].id
            ),
        ]
        db.session.add_all(replies)
        db.session.commit()
        print(f"Created {Reply.query.count()} replies")

        # ---------- Group summary (nice for demo logs) ----------
        print("\n=== Class Groups ===")
        for g in ClassGroup.query.all():
            maps = ClassGroupMap.query.filter_by(group_id=g.id).all()
            class_ids = [m.class_id for m in maps]
            members = Class.query.filter(Class.id.in_(class_ids)).all()
            uni_counts = {}
            for c in members:
                uni_name = c.university.name
                uni_counts[uni_name] = uni_counts.get(uni_name, 0) + 1
            print(f"- {g.label or g.signature}  (members: {len(members)})  unis: {uni_counts}")
            for c in members:
                print(f"    • {c.name}  — {c.university.name}")

        print("\n✅ Database seeded successfully!")
        print("\nSummary:")
        print(f"  - {University.query.count()} universities")
        print(f"  - {User.query.count()} users")
        print(f"  - {Tag.query.count()} tags")
        print(f"  - {Class.query.count()} classes")
        print(f"  - {Discussion.query.count()} discussions")
        print(f"  - {Reply.query.count()} replies")


if __name__ == "__main__":
    print("=" * 50)
    print("UniVerse Database Seeder")
    print("=" * 50)

    response = input("\nThis will clear all existing data. Continue? (yes/no): ")

    if response.lower() in ["yes", "y"]:
        clear_data()
        seed_data()
        
        print("\n All done! Your database is ready to use.")
        print(" Start your server with: python app.py")
        print(" View API docs at: http://localhost:5000/swagger\n")
    else:
        print("Seeding cancelled.")
