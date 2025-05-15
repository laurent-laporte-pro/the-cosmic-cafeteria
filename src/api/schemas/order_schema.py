from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validate
from api.models.order import Order
from api.app_extensions import db
from api.models.order import OrderStatus

class OrderSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        load_instance = True
        sqla_session = db.session

    status = fields.Field(dump_only=True)  # status always pending on create that's why is read only
    message = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.Length(max=500)
    )
    order_time = fields.DateTime(dump_only=True)
    completed_time = fields.DateTime(allow_none=True)
    hero_id = fields.Int(required=True)
    meal_id = fields.Int(required=True)
