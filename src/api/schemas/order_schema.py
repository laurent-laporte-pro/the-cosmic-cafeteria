from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validate, Schema
from api.models.order import Order
from api.app_extensions import db
from api.models.order import OrderStatus

class OrderSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        load_instance = True
        sqla_session = db.session
        include_fk = True

    status = fields.Method("get_status", dump_only=True) # thee field should be read only 
    message = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.Length(max=500)
    )
    order_time = fields.DateTime(dump_only=True)
    completed_time = fields.DateTime(allow_none=True)
    hero_id = fields.Int(required=True)
    meal_id = fields.Int(required=True)

    def get_status(self, obj):
        return obj.status.name 


class OrderDeleteActionSchema(Schema):
    """
    Schema to validate the action type when deleting an order.
    """

    action = fields.Str(
        required=True,
        validate=validate.OneOf(["cancel", "delete"]),
        error_messages={
            "required": "Action is required.",
            "validator_failed": "Action must be 'cancel' or 'delete'."
        }
    )
