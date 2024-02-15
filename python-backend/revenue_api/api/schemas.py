from marshmallow import Schema, fields, validate, EXCLUDE

class RevenueSchema(Schema):
    class Meta:
        unknown: EXCLUDE

    month = fields.String(
        required=True,
        validate=validate.OneOf(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        )
    revenue = fields.Integer(
        required=True,
        validate=validate.Range(min=0, max=1000000000, min_inclusive=True)
        )

class UpdateRevenueSchema(Schema):
    class Meta:
        unknown: EXCLUDE

    revenue = fields.Integer(
        required=True,
        validate=validate.Range(min=0, min_inclusive=True)
    )

class ListRevenueSchema(Schema):
    class Meta:
        unknown: EXCLUDE

    revenue = fields.List(fields.Nested(RevenueSchema), required=True)

class GetListRevenueParameters(Schema):
    class Meta:
        unknown: EXCLUDE

    minValue = fields.Integer(validate=validate.Range(min=0, max=1000000000, min_inclusive=True))