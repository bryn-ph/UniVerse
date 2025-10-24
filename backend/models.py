import uuid
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Uuid

db = SQLAlchemy()

class_tag = db.Table(
    "class_tag",
    db.Column("class_id", Uuid, db.ForeignKey("classes.id", ondelete="CASCADE"), primary_key=True),
    db.Column("tag_id",   Uuid, db.ForeignKey("tag.id", ondelete="CASCADE"),   primary_key=True),
)

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=db.func.now(),
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
        nullable=False
    )

    university_id = db.Column(
        Uuid,
        db.ForeignKey("university.id", ondelete="CASCADE"),
        nullable=False,
    )
    university = db.relationship(
        "University",
        backref=db.backref("users", lazy=True),
        passive_deletes=True,
    )

    def __repr__(self):
        return f"<User {self.email}>"

class University(db.Model):
    __tablename__ = "university"

    id = db.Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<University {self.name}>"

class Class(db.Model):
    __tablename__ = "classes"

    id = db.Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)

    university_id = db.Column(
        Uuid,
        db.ForeignKey("university.id", ondelete="CASCADE"),
        nullable=False
    )
    university = db.relationship(
        "University",
        backref=db.backref("classes", lazy=True),
        passive_deletes=True,
    )

    tags = db.relationship(
        "Tag",
        secondary=class_tag,
        passive_deletes=True,
        back_populates="classes",
        lazy=True
    )

    __table_args__ = (
        db.UniqueConstraint("university_id", "name", name="uq_class_uni_name"),
    )

    def __repr__(self):
        return f"<Class {self.name}>"

class Tag(db.Model):
    __tablename__ = "tag"

    id = db.Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50), nullable=False, unique=True, index=True)

    classes = db.relationship(
        "Class",
        secondary=class_tag,
        passive_deletes=True,
        back_populates="tags",
        lazy="selectin"
    )

    def __repr__(self):
        return f"<Tag {self.name}>"

class Discussion(db.Model):
    __tablename__ = "discussion"

    id = db.Column(Uuid, primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=db.func.now(),
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
        nullable=False,
    )

    user_id = db.Column(
        Uuid,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user = db.relationship(
        "User",
        backref=db.backref("discussions", lazy=True),
        passive_deletes=True,
    )

    class_id = db.Column(
        Uuid,
        db.ForeignKey("classes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    class_ = db.relationship(
        "Class",
        backref=db.backref("discussions", lazy=True),
        passive_deletes=True,
    )

    replies = db.relationship(
        "Reply",
        back_populates="discussion",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="selectin",
        order_by=lambda: Reply.created_at.asc(),
    )

    def __repr__(self):
        return f"<Discussion {self.title}>"

class Reply(db.Model):
    __tablename__ = "reply"

    id = db.Column(Uuid, primary_key=True, default=uuid.uuid4)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=db.func.now(),
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
        nullable=False
    )
    
    user_id = db.Column(
        Uuid,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user = db.relationship(
        "User",
        backref=db.backref("replies", lazy=True),
        passive_deletes=True,
    )

    discussion_id = db.Column(
        Uuid,
        db.ForeignKey("discussion.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    discussion = db.relationship(
        "Discussion",
        back_populates="replies",
    )

    def __repr__(self):
        return f"<Reply on Discussion {self.discussion_id}>"
