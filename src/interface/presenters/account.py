from marshmallow import Schema, fields


AccountPresenter = Schema.from_dict({
    'id': fields.Int(required=True),
    'created': fields.DateTime(required=True),
    'first_name': fields.Str(required=True),
    'last_name': fields.String(required=True),
    'number_identity': fields.String(required=True),
    'date_birth': fields.DateTime(required=True),
    'gender': fields.Integer(required=True),
    'status': fields.Integer(required=True)
})
