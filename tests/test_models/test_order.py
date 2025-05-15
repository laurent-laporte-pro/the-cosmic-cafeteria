import pytest
from api.models.order import Order, OrderStatus
from sqlalchemy.orm.attributes import flag_modified

def test_create_order(session, order, hero, meal):
    retrieved = session.get(Order, order.id)
    assert retrieved.hero_id == hero.id
    assert retrieved.meal_id == meal.id
    assert retrieved.status == OrderStatus.PENDING
    assert retrieved.message == "deliver"
    assert retrieved.completed_time is None


def test_update_order_status(session, order):
    order.status = OrderStatus.COMPLETED
    session.commit()
    updated = session.get(Order, order.id)
    assert updated.status == OrderStatus.COMPLETED


def test_update_order_message(session, order):
    order.message = "example"
    session.commit()
    updated = session.get(Order, order.id)
    assert updated.message == "example"


def test_delete_order(session, order):
    session.delete(order)
    session.commit()
    assert session.get(Order, order.id) is None
