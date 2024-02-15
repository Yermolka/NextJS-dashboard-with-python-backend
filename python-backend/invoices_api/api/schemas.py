from marshmallow import Schema, fields, validate, EXCLUDE
from datetime import date

class InvoiceSchema(Schema):
    class Meta:
        unknown: EXCLUDE

    customer_id = fields.String(
        required=True,
        allow_none=False
    )
    amount = fields.Integer(
        required=True,
        validate=validate.Range(min=1, max=1000000000, min_inclusive=True)
    )
    status = fields.String(
        required=False,
        validate=validate.OneOf(['pending', 'paid'])
    )
    date = fields.Date(default=date.today())

class ListInvoicesParameters(Schema):
    minAmount = fields.Integer(
        required=False,
        validate=validate.Range(min=1, max=1000000000, min_inclusive=True)
    )
    status = fields.String(
        required=False,
        validate=validate.OneOf(['pending', 'paid'])
    )

class GetInvoiceSchema(InvoiceSchema):
    class Meta:
        unknown: EXCLUDE

    id = fields.Integer(
        required=True
    )

class UpdateInvoiceSchema(Schema):
    class Meta:
        unknown: EXCLUDE

    amount = fields.Integer(
        required=False,
        validate=validate.Range(min=1, max=1000000000, min_inclusive=True)
    )
    status = fields.String(
        required=False,
        validate=validate.OneOf(['pending', 'paid'])
    )
    customer_id = fields.String(
        required=False
    )

class LatestInvoicesParameters(Schema):
    limit = fields.Integer(
        required=False,
        validate=validate.Range(min=1, min_inclusive=True, max=20, max_inclusive=True),
        default=5
    )

class LatestInvoicesSchema(Schema):
    class Meta:
        unknown: EXCLUDE

    amount = fields.Integer(
        required=True,
        validate=validate.Range(min=1, min_inclusive=True, max=1_000_000_000)
    )
    name = fields.String(
        required=True
    )
    image_url = fields.String(
        required=True,
        validate=validate.URL(relative=True, absolute=False)
    )
    email = fields.String(
        required=True
    )
    id = fields.Integer(
        required=True
    )

class ListLatestInvoicesSchema(Schema):
    class Meta:
        unknown: EXCLUDE

    invoices = fields.List(fields.Nested(LatestInvoicesSchema), required=True)

class ListInvoicesSchema(Schema):
    class Meta:
        unknown: EXCLUDE
    
    invoices = fields.List(fields.Nested(GetInvoiceSchema), required=True)

class InvoicesCountSchema(Schema):
    class Meta:
        unknown: EXCLUDE

    count = fields.Integer()

class InvoicesTotalSchema(Schema):
    class Meta:
        unknown: EXCLUDE

    total = fields.Integer()

class ListInvoicesFilteredParameters(Schema):
    query = fields.String(
        required=False, 
        default='')
    currentPage = fields.Integer(
        required=False,
        default=1,
        validate=validate.Range(min=1, min_inclusive=1, max=1_000_000_000))

class InvoiceFilteredSchema(Schema):
    class Meta:
        unknown: EXCLUDE

    id = fields.Integer(required=True)
    amount = fields.Integer(
        required=True,
        validate=validate.Range(min=1, min_inclusive=True, max=1_000_000_000)
    )
    date = fields.Date(required=True)
    status = fields.String(required=True)
    name = fields.String(required=True)
    email = fields.String(required=True)
    image_url = fields.String(
        required=True,
        validate=validate.URL(relative=True, absolute=False)
    )

class ListInvoicesFilteredSchema(Schema):
    class Meta:
        unknown: EXCLUDE

    invoices = fields.List(fields.Nested(InvoiceFilteredSchema), required=True)