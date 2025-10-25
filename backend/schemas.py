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

    # Enrolled classes
    classes = fields.Nested("ClassMiniSchema", many=True, dump_only=True)
    class_count = fields.Function(lambda obj: len(getattr(obj, "classes", [])))


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


class UserEnrollSchema(Schema):
    class_id = fields.UUID(required=True)


class UserEnrollBulkSchema(Schema):
    class_ids = fields.List(fields.UUID(), required=True)


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


class UniversityCreateSchema(Schema):
    name = fields.Str(required=True)


class UniversityUpdateSchema(Schema):
    name = fields.Str(required=True)

# ---------- CLASS GROUP ----------
class ClassGroupMiniSchema(Schema):
    id = fields.UUID()
    name = fields.Str()
    label = fields.Str()


class ClassGroupSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True)
    label = fields.Str()
    description = fields.Str()
    signature = fields.Str(dump_only=True)
    classes = fields.Nested("ClassSchema", many=True, dump_only=True, attribute="classes")
    class_count = fields.Function(lambda obj: len(getattr(obj, "classes", [])))


class ClassGroupCreateSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str()


class ClassGroupUpdateSchema(Schema):
    name = fields.Str()
    description = fields.Str()

class TagMiniSchema(Schema):
    id = fields.UUID()
    name = fields.Str()


class TagSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True)
    class_count = fields.Function(lambda obj: len(getattr(obj, "classes", [])))


class TagCreateSchema(Schema):
    name = fields.Str(required=True)


class TagUpdateSchema(Schema):
    name = fields.Str(required=True)


class ClassSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True)
    university_id = fields.UUID(dump_only=True)
    university = fields.Pluck(UniversityMiniSchema, "name", dump_only=True, attribute="university")
    class_group_id = fields.UUID(dump_only=True)
    class_group = fields.Pluck(ClassGroupMiniSchema, "name", dump_only=True, attribute="class_group")
    discussion_count = fields.Function(lambda obj: len(getattr(obj, "discussions", [])))
    enrolled_count = fields.Function(lambda obj: len(getattr(obj, "enrolled_users", [])))
    tags = fields.Nested(TagMiniSchema, many=True, dump_only=True)
    group_id = fields.Function(lambda obj: str(obj.group_map.group_id) if getattr(obj, "group_map", None) else None)
    group_label = fields.Function(
        lambda obj: getattr(getattr(getattr(obj, "group_map", None), "class_group", None), "label", None)
    )


class ClassCreateSchema(Schema):
    name = fields.Str(required=True)
    university_id = fields.UUID(required=True)
    class_group_id = fields.UUID(required=True)
    tag_ids = fields.List(fields.UUID(), load_only=True)


class ClassUpdateSchema(Schema):
    name = fields.Str()
    class_group_id = fields.UUID()
    tag_ids = fields.List(fields.UUID())


# ---------- REPLY ----------
class ReplySchema(Schema):
    id = fields.UUID(dump_only=True)
    body = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)

    discussion_id = fields.UUID(dump_only=True)
    user_id = fields.UUID(dump_only=True)

    # Related / derived info
    author = fields.Pluck(UserBaseSchema, "name", dump_only=True, attribute="user")
    discussion_title = fields.Pluck("DiscussionSchema", "title", dump_only=True, attribute="discussion")


class ReplyCreateSchema(Schema):
    body = fields.Str(required=True)
    user_id = fields.UUID(required=True)
    discussion_id = fields.UUID(required=True)


class ReplyUpdateSchema(Schema):
    body = fields.Str(required=True)


class ReplyQuerySchema(Schema):
    discussion_id = fields.UUID()
    user_id = fields.UUID()


# ---------- DISCUSSION ----------
class DiscussionSchema(Schema):
    id = fields.UUID(dump_only=True)
    title = fields.Str(required=True)
    body = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)

    user_id = fields.UUID(dump_only=True)
    class_id = fields.UUID(dump_only=True)

    author = fields.Pluck(UserBaseSchema, "name", dump_only=True, attribute="user")
    class_name = fields.Pluck(ClassMiniSchema, "name", dump_only=True, attribute="class_")
    university = fields.Pluck(UniversityMiniSchema, "name", dump_only=True, attribute="class_.university")
    replies = fields.Nested(ReplySchema, many=True, dump_only=True)
    reply_count = fields.Function(lambda obj: len(getattr(obj, "replies", [])))


class DiscussionCreateSchema(Schema):
    title = fields.Str(required=True)
    body = fields.Str(required=True)
    user_id = fields.UUID(required=True)
    class_id = fields.UUID(required=True)


class DiscussionUpdateSchema(Schema):
    title = fields.Str()
    body = fields.Str()


class DiscussionQuerySchema(Schema):
    class_id = fields.UUID()
    university_id = fields.UUID()
    user_id = fields.UUID()
    q = fields.Str()