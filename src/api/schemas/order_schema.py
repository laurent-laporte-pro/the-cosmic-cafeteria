from api.extensions import ma
from api.models.Order import Order
from api.models.order_status import OrderStatus
from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        include_fk = True  
        load_instance = True  
    