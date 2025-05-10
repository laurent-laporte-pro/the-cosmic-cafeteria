# schemas/order_schema.py
from marshmallow import fields, validate
from marshmallow_enum import EnumField  # pip install marshmallow-enum
from api.extensions import ma
from api.models import Order, OrderStatus

class OrderSchema(ma.SQLAlchemyAutoSchema):
    status = EnumField(OrderStatus, by_value=True)
    
    class Meta:
        model = Order
        include_fk = True  # Includes foreign keys
        load_instance = True  # Allows deserialization to model instances