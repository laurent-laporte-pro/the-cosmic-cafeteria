import pytest
from sqlalchemy.orm import Session
from api.models.order import Order, OrderStatus
from api.models.hero import Hero
from api.models.meal import Meal
from api.views.order_service import process_order_logic


def test_process_order_conflict(session: Session, setup_data):
    order = setup_data["order_conflict"]
    status = process_order_logic(session, order.id)
    assert status == OrderStatus.CANCELLED.name

    updated_order = session.get(Order, order.id)
    assert "allergic" in updated_order.message.lower()
    assert updated_order.status == OrderStatus.CANCELLED


def test_process_order_safe(session: Session, setup_data):
    order = setup_data["order_safe"]
    status = process_order_logic(session, order.id)
    assert status == OrderStatus.COMPLETED.name

    updated_order = session.get(Order, order.id)
    assert updated_order.message == "Success"
    assert updated_order.status == OrderStatus.COMPLETED
