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
    """Seed the database with sample data (expanded text, student-made threads only)"""
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

        print("Creating cross-uni 'essentially same' classes...")

        # Family 1: Operating Systems (variants across unis)
        uom_os   = Class(name="Operating Systems",                             university_id=uni1.id)
        unsw_os  = Class(name="Systems & Concurrency",                         university_id=uni2.id)
        anu_os   = Class(name="Operating Systems Principles",                  university_id=uni3.id)
        rmit_os  = Class(name="Operating Systems and Systems Programming",     university_id=uni4.id)

        for c in (uom_os, unsw_os, anu_os, rmit_os):
            c.tags.extend([tags[0], tags[3]])  # Computer Science, Engineering

        # Family 2: Database Systems (variants across unis)
        uom_db2  = Class(name="Database Systems",                              university_id=uni1.id)
        unsw_db2 = Class(name="Relational Databases",                          university_id=uni2.id)
        anu_db2  = Class(name="Data Management Systems",                       university_id=uni3.id)
        rmit_db2 = Class(name="Intro to Relational Databases",                 university_id=uni4.id)

        for c in (uom_db2, unsw_db2, anu_db2, rmit_db2):
            c.tags.extend([tags[0], tags[9]])  # Computer Science, Data Science

        # Family 3: Software Requirements/Design (variants across unis)
        uom_req  = Class(name="Software Requirements & Design",                university_id=uni1.id)
        unsw_req = Class(name="Requirements Engineering",                      university_id=uni2.id)
        anu_req  = Class(name="Software Analysis & Design",                    university_id=uni3.id)
        rmit_req = Class(name="Software Design Studio",                        university_id=uni4.id)

        for c in (uom_req, unsw_req, anu_req, rmit_req):
            c.tags.extend([tags[0], tags[3]])  # Computer Science, Engineering

        new_classes = [
            uom_os, unsw_os, anu_os, rmit_os,
            uom_db2, unsw_db2, anu_db2, rmit_db2,
            uom_req, unsw_req, anu_req, rmit_req,
        ]

        db.session.add_all(new_classes)
        db.session.commit()
        print(f"Added {len(new_classes)} cross-uni variant classes")

        # --- Discussions & Replies for the new classes (student-made, varied tone) ---
        print("Creating discussions for the new classes...")

        # Helper to rotate users for authors/repliers without self-replies
        user_order = [users[0], users[1], users[2], users[3], users[4], users[5], users[6], users[7], users[8], users[9]]
        def author(idx): return user_order[idx % len(user_order)]
        def replier(idx): return user_order[(idx + 3) % len(user_order)]  # offset to avoid self

        _discussions = []
        _replies = []

        # ----- Operating Systems family -----
        _os_threads = [
            (
                uom_os,
                "Scheduling: RR vs MLFQ in practice",
                "Working on the lab and curious how round-robin compares to multi-level feedback queues once you factor in I/O bound tasks. "
                "Any gotchas when tuning time slices so we don’t starve long CPU jobs?"
            ),
            (
                uom_os,
                "Deadlocks: resource ordering vs banker’s algorithm",
                "For the assignment design doc, would you justify deadlock avoidance with a strict resource ordering or implement a banker-style check? "
                "Which is more defensible in a code review?"
            ),
            (
                unsw_os,
                "Concurrency bugs you actually hit this week",
                "Share the minimal snippets where your mutex/condition variable ordering went wrong. "
                "Seeing real failure modes helps more than pseudo-code 🤕."
            ),
            (
                anu_os,
                "Paging vs segmentation: exam tips",
                "What’s the fastest way to avoid off-by-one page table errors on the exam? "
                "Rules of thumb for translating VA→PA under two-level paging appreciated."
            ),
            (
                rmit_os,
                "Syscalls performance: when does context switch dominate?",
                "Profiling a toy web server — at what request size/shape do context switches become the bottleneck vs user-space parsing?"
            ),
        ]

        for i, (klass, title, body) in enumerate(_os_threads):
            d = Discussion(title=title, body=body, user_id=author(i).id, class_id=klass.id)
            _discussions.append(d)

        # ----- Database Systems family -----
        _db_threads = [
            (
                uom_db2,
                "Indexing strategy for mix of range + equality filters",
                "Given queries mixing `WHERE status = ? AND created_at BETWEEN ? AND ?`, "
                "is a composite (status, created_at) B-tree enough or would you split and lean on CLUSTERing?"
            ),
            (
                unsw_db2,
                "Normal forms: where to stop in real apps?",
                "Do you actually push to BCNF in production schemas, or is 3NF + a couple of deliberate denorms more realistic?"
            ),
            (
                anu_db2,
                "JOIN order and planner hints",
                "On a skewed dataset, the planner keeps choosing a bad hash join order. "
                "Any safe hints or stats tweaks to nudge it without going full manual plan?"
            ),
            (
                rmit_db2,
                "Transactions: READ COMMITTED vs REPEATABLE READ",
                "For our project workload (lots of short reads + occasional updates), which isolation level is the sweet spot?"
            ),
        ]

        for j, (klass, title, body) in enumerate(_db_threads, start=len(_os_threads)):
            d = Discussion(title=title, body=body, user_id=author(j).id, class_id=klass.id)
            _discussions.append(d)

        # ----- Requirements/Design family -----
        _req_threads = [
            (
                uom_req,
                "User stories vs use cases (for this assignment)",
                "Marker guidance seems vague — would you write both, or lean into one with acceptance criteria and rationale?"
            ),
            (
                unsw_req,
                "Non-functional reqs: how to make them testable",
                "Looking for examples of turning 'fast', 'secure', 'accessible' into measurable acceptance tests for the rubric."
            ),
            (
                anu_req,
                "UML granularity: class vs component diagrams",
                "What level of detail do you include so it’s not spaghetti but still defensible in the demo Q&A?"
            ),
            (
                rmit_req,
                "Design reviews: lightweight but useful checklist?",
                "Share your short checklist that actually catches issues before implementation — no 10-page templates please."
            ),
        ]

        for k, (klass, title, body) in enumerate(_req_threads, start=len(_os_threads)+len(_db_threads)):
            d = Discussion(title=title, body=body, user_id=author(k).id, class_id=klass.id)
            _discussions.append(d)

        db.session.add_all(_discussions)
        db.session.commit()
        print(f"Added {len(_discussions)} discussions for new classes")

        # --- Replies (at least one per new discussion; varied, student tone) ---
        for idx, d in enumerate(_discussions):
            _replies.append(Reply(
                body=(
                    # short, useful replies; no placeholders
                    "Quick take: start with a simple baseline, measure, and only then add complexity. "
                    "Also drop links/screenshots in the repo so others can reproduce your results."
                ),
                user_id=replier(idx).id,
                discussion_id=d.id
            ))

        # A few extra richer replies sprinkled across threads
        _extra_replies = [
            Reply(
                body="For RR vs MLFQ: cap the number of queues and promote I/O-bound tasks aggressively; it smooths latency without starving CPU hogs.",
                user_id=users[4].id,  # Eve
                discussion_id=_discussions[0].id
            ),
            Reply(
                body="Deadlocks: resource ordering is easier to reason about in reviews; banker’s is fine for teaching but noisy in prod unless well-bounded.",
                user_id=users[6].id,  # Grace
                discussion_id=_discussions[1].id
            ),
            Reply(
                body="3NF is a great pragmatic target. Denorm selectively for read paths with real perf data; document the rationale next to the schema.",
                user_id=users[9].id,  # Jack
                discussion_id=_discussions[len(_os_threads)].id  # first DB thread
            ),
            Reply(
                body="Testable NFRs: e.g., 'P95 API latency < 250ms under 200 RPS' or 'WCAG 2.2 AA: all interactive elements keyboard-navigable with focus state'.",
                user_id=users[8].id,  # Isla
                discussion_id=_discussions[len(_os_threads)+len(_db_threads)+1].id  # second Req/Design thread
            ),
        ]

        _replies.extend(_extra_replies)
        db.session.add_all(_replies)
        db.session.commit()
        print(f"Added {len(_replies)} replies for new discussions")

        # ---------- Group classes across universities ----------
        print("Assigning classes to cross-university groups…")
        for c in Class.query.all():
            assign_class_to_group(c)
        print(f"Groups created: {ClassGroup.query.count()}")

        # ---------- Discussions (expanded bodies; student-made, realistic mix) ----------
        print("Creating discussions...")
        discussions = [
            # CS101
            Discussion(
                title="How do I install Python?",
                body=(
                    "I’m getting mixed advice from Reddit vs lecture slides. "
                    "What’s the cleanest way to install Python 3 with pip and set up a virtualenv on Windows/macOS/Linux?\n\n"
                    "If you can, please include steps that avoid PATH chaos and how to verify the install (`python --version`, `pip --version`)."
                ),
                user_id=users[0].id,
                class_id=cs101.id
            ),
            Discussion(
                title="Understanding recursion",
                body=(
                    "Factorials make sense but I still struggle to *see* the call stack for recursion. "
                    "When do you reach for recursion over loops in real code? \n\n"
                    "Any tips for debugging or tracing recursive calls would help heaps."
                ),
                user_id=users[1].id,
                class_id=cs101.id
            ),

            # CS229
            Discussion(
                title="Gradient descent not converging",
                body=(
                    "My loss curve plateaus then oscillates for linear regression. I’ve tried smaller learning rates and mini-batches. \n\n"
                    "What else should I check — feature scaling, initialization, or bugs in my gradient calculation?"
                ),
                user_id=users[6].id,
                class_id=cs229.id
            ),
            Discussion(
                title="Best resources for understanding neural networks?",
                body=(
                    "Looking for a resource that explains forward/backprop clearly with visuals *and* the math. "
                    "Videos, books, interactive demos — what actually clicked for you?"
                ),
                user_id=users[0].id,
                class_id=cs229.id
            ),

            # MIT AI (UNSW)
            Discussion(
                title="Study group for the upcoming assessment",
                body=(
                    "Anyone keen to meet twice this week to work through past papers? "
                    "We can split topics and rotate explainers. Drop times you’re free."
                ),
                user_id=users[2].id,
                class_id=mit_ai.id
            ),
            Discussion(
                title="A* search algorithm question",
                body=(
                    "I know A* is optimal with an admissible heuristic, but I’m fuzzy on why consistency matters. "
                    "Could someone sketch the intuition and any practical tie-breaking tips?"
                ),
                user_id=users[3].id,
                class_id=mit_ai.id
            ),

            # ANU DS
            Discussion(
                title="Project partners needed",
                body=(
                    "Forming a small team (3–4) for the term project — data cleaning, model eval, tiny dashboard. "
                    "If you like docs/tests, even better. What part would you like to own?"
                ),
                user_id=users[4].id,
                class_id=anu_ds.id
            ),
            Discussion(
                title="Pandas vs NumPy — when to use which?",
                body=(
                    "I keep bouncing between DataFrames and ndarrays. "
                    "Where do you draw the line, especially for groupby/join vs custom numerical ops?"
                ),
                user_id=users[5].id,
                class_id=anu_ds.id
            ),

            # RMIT
            Discussion(
                title="Best tools for building secure web apps",
                body=(
                    "Looking for a practical stack for auth, sessions, CSRF, input validation. "
                    "How do you handle secrets locally vs prod without chaos?"
                ),
                user_id=users[8].id,
                class_id=rmit_cyber.id
            ),
            Discussion(
                title="How to manage company data in Information Systems",
                body=(
                    "Designing an IS for a small biz: what’s your go-to for modeling, backups, access control, and reporting? "
                    "Bonus: onboarding non-tech staff without overwhelming them."
                ),
                user_id=users[9].id,
                class_id=rmit_is.id
            ),

            # --- NEW student-made threads for classes that had none ---

            # Linear Algebra (study help)
            Discussion(
                title="Exam prep: eigenvalues/eigenvectors on past papers",
                body=(
                    "Anyone else finding the eigenvalue proofs a bit gnarly? "
                    "I’m okay with computations but the theory questions are rough. "
                    "What’s your strategy for quickly identifying diagonalizable matrices and spotting trick questions?"
                ),
                user_id=users[7].id,  # Henry
                class_id=math51.id
            ),

            # Software Engineering (casual chatter)
            Discussion(
                title="How’s everyone managing the workload + tooling?",
                body=(
                    "Between issues, PRs, tests, and sprints, I’m drowning. "
                    "What combo of Git workflow + task board + CI checks is realistic for this class? "
                    "Share your setup, please!"
                ),
                user_id=users[6].id,  # Grace
                class_id=melb_se.id
            ),

            # Intro to Databases (concept clarification)
            Discussion(
                title="Foreign keys + cascade delete: when to actually use it?",
                body=(
                    "I get how FK constraints work, but I’m nervous about `ON DELETE CASCADE`. "
                    "When is it appropriate vs dangerous in real systems? "
                    "Would you prefer soft deletes instead?"
                ),
                user_id=users[0].id,  # Alice
                class_id=melb_db.id
            ),

            # Algorithms & DS (study help)
            Discussion(
                title="Asymptotic analysis on Assignment 2 (proof structure)",
                body=(
                    "For the divide-and-conquer question, what’s a clean way to structure the Big-O proof? "
                    "Master theorem vs full recurrence solve — which does the marker expect?"
                ),
                user_id=users[2].id,  # Charlie
                class_id=mit_cs.id
            ),

            # Robotics (concept/practice)
            Discussion(
                title="PID tuning tips for the line-follower lab",
                body=(
                    "I’m over/undershooting corners. Any rule-of-thumb starting values for P/I/D, "
                    "and how do you iterate without chasing your tail all lab?"
                ),
                user_id=users[3].id,  # Diana
                class_id=unsw_robotics.id
            ),

            # Computer Networks (study help)
            Discussion(
                title="Subnetting speed drills + CIDR cheats",
                body=(
                    "What helped you get fast at subnetting? "
                    "Do you memorize masks or use a mental grid? "
                    "Share tricks or worksheets that actually worked."
                ),
                user_id=users[7].id,  # Henry
                class_id=unsw_networks.id
            ),

            # Quantum Mechanics (concept clarification)
            Discussion(
                title="Normalization + bra–ket notation intuition",
                body=(
                    "I understand the algebra, but I’m missing the *feel* for normalization in QM. "
                    "How do you interpret ⟨ψ|ψ⟩=1 physically and keep track of inner products without getting lost?"
                ),
                user_id=users[4].id,  # Eve
                class_id=anu_physics.id
            ),

            # Statistical Methods (study help)
            Discussion(
                title="Choosing the right test: ANOVA vs t-test vs Mann–Whitney",
                body=(
                    "Cheat-sheet for deciding which test to use? "
                    "Assumptions to check first (normality, equal variances), and sample-size gotchas appreciated."
                ),
                user_id=users[5].id,  # Frank
                class_id=anu_stats.id
            ),

            # Quantum Computing (casual/concept)
            Discussion(
                title="Qubit intuition: Bloch sphere made simple?",
                body=(
                    "Any visual or mnemonic that helped qubits click? "
                    "Superposition is fine, but I’m hazy on rotations and measurement collapse on the Bloch sphere."
                ),
                user_id=users[1].id,  # Bob
                class_id=anu_qc.id
            ),
        ]
        db.session.add_all(discussions)
        db.session.commit()
        print(f"Created {Discussion.query.count()} discussions")

        # ---------- Replies (expanded bodies; at least one per discussion) ----------
        print("Creating replies...")
        replies = [
            # CS101
            Reply(
                body=(
                    "Windows: use the official installer and tick ‘Add python.exe to PATH’. "
                    "macOS: `brew install python`. Linux: use your package manager. "
                    "Then `python -m venv .venv` and activate. Verify with `python --version` and `pip --version`."
                ),
                user_id=users[1].id,
                discussion_id=discussions[0].id
            ),
            Reply(
                body=(
                    "If you juggle versions, `pyenv` is worth it. "
                    "It prevents PATH weirdness and keeps projects isolated cleanly."
                ),
                user_id=users[6].id,
                discussion_id=discussions[0].id
            ),
            Reply(
                body=(
                    "Write the base case first. Then ensure each recursive step strictly reduces the input size. "
                    "Printing call depth (indentation) is a great way to build intuition quickly."
                ),
                user_id=users[0].id,
                discussion_id=discussions[1].id
            ),

            # CS229
            Reply(
                body=(
                    "Try standardizing features and lowering LR by 10x. "
                    "Plot train vs val loss; if they diverge, regularize or check data leakage."
                ),
                user_id=users[0].id,
                discussion_id=discussions[2].id
            ),
            Reply(
                body=(
                    "For resources: 3Blue1Brown for intuition, then Goodfellow et al. for rigor. "
                    "Pairing the two made backprop finally click for me."
                ),
                user_id=users[1].id,
                discussion_id=discussions[3].id
            ),

            # MIT AI
            Reply(
                body="I can do Wed/Fri evenings. Happy to lead heuristic design.",
                user_id=users[3].id,
                discussion_id=discussions[4].id
            ),
            Reply(
                body=(
                    "Consistency means your heuristic obeys triangle inequality-ish behavior. "
                    "It guarantees non-decreasing f along paths, so the first time you reach the goal it’s optimal."
                ),
                user_id=users[2].id,
                discussion_id=discussions[5].id
            ),

            # ANU DS
            Reply(
                body=(
                    "I can own evaluation + dashboard. Let’s define a simple data contract early to avoid schema drift."
                ),
                user_id=users[5].id,
                discussion_id=discussions[6].id
            ),
            Reply(
                body=(
                    "Rule of thumb: Pandas for labeled/tabular ops (groupby/join), NumPy for raw n-dim arrays and custom math. "
                    "Convert at module boundaries to keep code clean."
                ),
                user_id=users[4].id,
                discussion_id=discussions[7].id
            ),

            # RMIT
            Reply(
                body=(
                    "Short-lived sessions, CSRF protection, strict input validation, vetted auth lib. "
                    "Use env vars locally, a secrets manager in prod."
                ),
                user_id=users[8].id,
                discussion_id=discussions[8].id
            ),
            Reply(
                body=(
                    "Normalized schema + automated backups with retention. "
                    "Docs with screenshots and short Looms help non-tech folks a lot."
                ),
                user_id=users[9].id,
                discussion_id=discussions[9].id
            ),

            # NEW class threads — ensure at least one reply each (different user)
            Reply(
                body=(
                    "For eigen stuff: practice recognizing repeated eigenvalues and check geometric multiplicity. "
                    "A quick diagonalizability test: compare algebraic vs geometric multiplicities."
                ),
                user_id=users[6].id,  # Grace replies to Henry
                discussion_id=discussions[10].id
            ),
            Reply(
                body=(
                    "We use trunk-based with short-lived branches, conventional commits, and a minimal PR template. "
                    "CI runs lint/tests on PR; keeps things moving without ceremony."
                ),
                user_id=users[0].id,  # Alice replies to Grace
                discussion_id=discussions[11].id
            ),
            Reply(
                body=(
                    "`ON DELETE CASCADE` is fine for true ownership (e.g., child has no meaning without parent). "
                    "For audit-heavy domains, prefer soft deletes and archival."
                ),
                user_id=users[6].id,  # Grace replies to Alice
                discussion_id=discussions[12].id
            ),
            Reply(
                body=(
                    "If allowed, the Master Theorem is perfect for the stated recurrence. "
                    "Otherwise, show the expansion a couple rounds then prove by induction."
                ),
                user_id=users[3].id,  # Diana replies to Charlie
                discussion_id=discussions[13].id
            ),
            Reply(
                body=(
                    "Start with P high enough to follow the line, D to damp overshoot, I tiny or zero. "
                    "Change one knob at a time and log values you try."
                ),
                user_id=users[2].id,  # Charlie replies to Diana
                discussion_id=discussions[14].id
            ),
            Reply(
                body=(
                    "Memorize /24 /25 /26 masks and derive the rest. "
                    "Practice with random IPs daily — speed comes from repetition."
                ),
                user_id=users[7].id,  # Henry replies to (Henry posted) — avoid self: pick Eve instead
                discussion_id=discussions[15].id
            ),
            Reply(
                body=(
                    "Think of ⟨ψ|ψ⟩ as total probability 1 when measured. "
                    "Bra–ket is just inner products in a complex vector space — the notation condenses a lot of algebra."
                ),
                user_id=users[5].id,  # Frank replies to Eve
                discussion_id=discussions[16].id
            ),
            Reply(
                body=(
                    "Checklist: normality (Q–Q plot), equal variances (Levene), independence; "
                    "if assumptions fail, consider nonparametric alternatives."
                ),
                user_id=users[4].id,  # Eve replies to Frank
                discussion_id=discussions[17].id
            ),
            Reply(
                body=(
                    "Bloch sphere: imagine a unit vector pointing to your qubit’s state. "
                    "Rotations are just unitary ops moving that vector; measurement projects it to poles."
                ),
                user_id=users[9].id,  # Jack replies to Bob
                discussion_id=discussions[18].id
            ),
        ]

        # Fix one potential self-reply above (networks thread) by swapping replier if needed
        # Replace the replier for discussions[15] (unsw_networks) with Eve explicitly:
        replies[-6] = Reply(
            body=(
                "Memorize /24 /25 /26 masks and derive the rest. "
                "Practice with random IPs daily — speed comes from repetition."
            ),
            user_id=users[4].id,  # Eve replies (not Henry)
            discussion_id=discussions[15].id
        )

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
