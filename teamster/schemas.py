from marshmallow import Schema, fields, pre_dump


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


class ScheduleList(fields.Nested):
    def _serialize(self, value, attr, obj):
        if attr == 'schedule' and not value:
            value = []
        return super()._serialize(value, attr, obj)


class ResponseUserSchema(Schema):
    id = fields.String()
    name = fields.String()
    birthday = fields.Date()
    phone = fields.String()
    email = fields.String()
    schedule = ScheduleList(ResponseScheduleSchema, many=True)


class AddScheduleSchema(Schema):
    str_type = fields.String(required=True, validate=lambda val: val in ('start', 'end', 'eat', 'rest'))
    time_start = fields.Time(required=True)
    time_end = fields.Time(required=True)
