from marshmallow import Schema, fields, validate, EXCLUDE

class CustomerSchema(Schema):
    class Meta:
        unknown: EXCLUDE

    name = fields.String(
        required=True,
        validate=validate.Length(min=1)
    )
    email = fields.String(
        required=True,
        validate=validate.Email()
    )
    image_url = fields.String(
        required=True,
        validate=validate.URL(relative=True, absolute=False)
    )

class UpdateCustomerSchema(Schema):
    class Meta:
        unknown: EXCLUDE

    name = fields.String(
        validate=validate.Length(min=1)
    )
    email = fields.String(
        validate=validate.Email()
    )
    image_url = fields.String(
        validate=validate.URL(relative=True, absolute=False)
    )

class ListCustomersParameters(Schema):
    pass

class GetCustomerSchema(CustomerSchema):
    id = fields.String(
        required=True
    )

class ListCustomersSchema(Schema):
    class Meta:
        unknown: EXCLUDE

    customers = fields.List(fields.Nested(GetCustomerSchema), required=True)

class CustomerCountSchema(Schema):
    class Meta:
        unknown: EXCLUDE

    count = fields.Integer()

class GetCustomerParameters(Schema):
    pass

class CustomersFilteredParameters(Schema):
    class Meta:
        unknown: EXCLUDE

    query = fields.String(required=False)

class GetFilteredCustomerSchema(Schema):
    class Meta:
        unknown: EXCLUDE

    id = fields.String(
        required=True
    )
    name = fields.String(
        required=True
    )
    email = fields.String(
        required=True
    )
    image_url = fields.String(
        required=True
    )
    total_invoices = fields.Integer(
        required=True
    )
    total_pending = fields.Integer(
        required=True
    )
    total_paid = fields.Integer(
        required=True
    )

class ListCustomersFilteredSchema(Schema):
    class Meta:
        unknown: EXCLUDE

    customers = fields.List(fields.Nested(GetFilteredCustomerSchema), required=True)