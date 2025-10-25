from marshmallow import Schema, fields

# ---------- Reply ----------
class ReplySchema(Schema):
    id = fields.UUID(dump_only=True)
    body = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    author = fields.Str(dump_only=True)
    author_id = fields.UUID(dump_only=True)
    discussion_id = fields.UUID(required=True)

# ---------- Discussion ----------
class DiscussionSchema(Schema):
    id = fields.UUID(dump_only=True)
    title = fields.Str(required=True)
    body = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    author = fields.Str(dump_only=True)
    university = fields.Str(dump_only=True)
    class_name = fields.Str(dump_only=True)
    reply_count = fields.Int(dump_only=True)
    user_id = fields.UUID(required=True, load_only=True)
    class_id = fields.UUID(required=True, load_only=True)
    replies = fields.Nested(ReplySchema, many=True, dump_only=True)

# ---------- User ----------
class UserBaseSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    university_id = fields.UUID(required=True, load_only=True)
    university = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

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


# ---------- University ----------
class UniversitySchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True)
    user_count = fields.Int(dump_only=True)
    class_count = fields.Int(dump_only=True)


class ClassSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True)
    university_id = fields.UUID(required=True)
    discussion_count = fields.Int(dump_only=True)
    tags = fields.List(fields.Dict(), dump_only=True)


