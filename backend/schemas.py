from marshmallow import Schema, fields

# ---------- USER ----------
class UniversityMiniSchema(Schema):
    id = fields.UUID()
    name = fields.Str()


class UserBaseSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    created_at = fields.DateTime(dump_only=True)

    # direct FK for input, pluck for output
    university_id = fields.UUID(load_only=True)
    university = fields.Pluck(UniversityMiniSchema, "name", dump_only=True)


class UserCreateSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    university_id = fields.UUID(required=True)

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class UserUpdateSchema(Schema):
    name = fields.Str()
    password = fields.Str(load_only=True)


# ---------- UNIVERSITY ----------
class ClassMiniSchema(Schema):
    id = fields.UUID()
    name = fields.Str()


class UniversitySchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True)
    users = fields.Nested(UserBaseSchema, many=True, dump_only=True)
    classes = fields.Nested(ClassMiniSchema, many=True, dump_only=True)

    # automatically derived counts
    user_count = fields.Function(lambda obj: len(getattr(obj, "users", [])))
    class_count = fields.Function(lambda obj: len(getattr(obj, "classes", [])))


class ClassSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True)
    university_id = fields.UUID(required=True)
    university = fields.Pluck(UniversityMiniSchema, "name", dump_only=True)
    discussion_count = fields.Function(lambda obj: len(getattr(obj, "discussions", [])))
    tags = fields.List(fields.Str(), dump_only=True)


# ---------- REPLY ----------
class ReplySchema(Schema):
    id = fields.UUID(dump_only=True)
    body = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)

    discussion_id = fields.UUID(required=True, load_only=True)
    user_id = fields.UUID(required=True, load_only=True)

    # Related / derived info
    author = fields.Pluck(UserBaseSchema, "name", dump_only=True)
    discussion_title = fields.Pluck("DiscussionSchema", "title", dump_only=True)


# ---------- DISCUSSION ----------
class DiscussionSchema(Schema):
    id = fields.UUID(dump_only=True)
    title = fields.Str(required=True)
    body = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)

    user_id = fields.UUID(required=True, load_only=True)
    class_id = fields.UUID(required=True, load_only=True)

    author = fields.Pluck(UserBaseSchema, "name", dump_only=True)
    class_name = fields.Pluck(ClassMiniSchema, "name", dump_only=True)
    university = fields.Pluck(UniversityMiniSchema, "name", dump_only=True, attribute="class_.university")
    replies = fields.Nested(ReplySchema, many=True, dump_only=True)
    reply_count = fields.Function(lambda obj: len(getattr(obj, "replies", [])))
