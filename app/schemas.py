from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(load_only=True, required=True)

class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    genre = fields.Str()
    year_published = fields.Int()
    summary = fields.Str()

class ReviewSchema(Schema):
    id = fields.Int(dump_only=True)
    book_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    review_text = fields.Str(required=True)
    rating = fields.Int(required=True)
