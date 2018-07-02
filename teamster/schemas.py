from marshmallow import Schema, fields


class CreateUserSchema(Schema):
    name = fields.String(required=True)
    birthday = fields.Date()
    phone = fields.String(
        validate=lambda val: all(x.isnumeric() or x in '+-() ' for x in val)
    )
    email = fields.Email()


class ResponseScheduleSchema(Schema):
    str_type = fields.String()
    time_start = fields.Time()
    time_end = fields.Time()


class ResponseUserSchema(Schema):
    name = fields.String(required=True)
    birthday = fields.Date()
    phone = fields.String()
    email = fields.String()
    schedule = fields.Nested(ResponseScheduleSchema, many=True)


class AddScheduleSchema(Schema):
    str_type = fields.String(required=True, validate=lambda val: val in ('start', 'end', 'eat', 'rest'))
    time_start = fields.Time(required=True)
    time_end = fields.Time(required=True)
