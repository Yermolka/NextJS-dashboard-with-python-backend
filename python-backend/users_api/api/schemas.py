from marshmallow import Schema, fields, validate, EXCLUDE

class UserSchema(Schema):
    class Meta:
        unknown: EXCLUDE

    name = fields.String(
        required=True,
        validate=validate.Length(min=2, max=30)
    )
    email = fields.String(
        required=True,
        validate=validate.Email()
    )
    password = fields.String(
        required=True,
        validate=validate.Length(min=6)
    )

class GetUserSchema(UserSchema):
    id = fields.UUID(
        required=True
    )

class UpdateUserSchema(Schema):
    class Meta:
        unknown: EXCLUDE

    name = fields.String(
        required=False,
        validate=validate.Length(min=2, max=30)
    )
    email = fields.String(
        required=False,
        validate=validate.Email()
    )
    password = fields.String(
        required=False,
        validate=validate.Length(min=6)
    )