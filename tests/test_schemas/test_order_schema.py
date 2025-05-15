import pytest
from marshmallow import ValidationError
from api.models.order import OrderStatus



def test_order_schema_valid(order_schema):
    data = {
        "hero_id": 1,
        "meal_id": 2,
        "message": "example_message"
        # status should be ignored on load, set automatically to PENDING in model
    }
    order = order_schema.load(data)
    assert order.hero_id == 1
    assert order.meal_id == 2
    assert order.message == "example_message"
    # check if the created order is in pending status 
    assert order.status == OrderStatus.PENDING
   

def test_order_schema_missing_required_fields(order_schema):
    data = {
        "message": "example_message"
    }
    with pytest.raises(ValidationError) as excinfo:
        order_schema.load(data)
    errors = excinfo.value.messages
    assert "hero_id" in errors
    assert "meal_id" in errors

def test_order_schema_message_optional(order_schema):
    data = {
        "hero_id": 1,
        "meal_id": 2,
        # no message
    }
    order = order_schema.load(data)
    assert order.message is None
