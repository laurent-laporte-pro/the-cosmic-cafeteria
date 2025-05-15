import pytest
from flask import url_for
from api.models import Hero, Meal, Order, OrderStatus
from unittest.mock import patch, MagicMock
from worker.tasks import process_order_task


@pytest.mark.parametrize("sleep_time", [1, 2, 3, 4, 5])
@patch("worker.tasks.time.sleep", autospec=True)
@patch("worker.tasks.process_order_logic", autospec=True)
@patch("worker.tasks.logger")
def test_create_order(mock_logger, mock_process_logic, mock_sleep, sleep_time, client, hero, meal):

    mock_sleep.return_value = None
    mock_process_logic.return_value = "COMPLETED"

    # Patch random.uniform to return controlled sleep_time
    with patch("worker.tasks.random.uniform", return_value=sleep_time):
        process_order_task(123)


    payload = {
        "hero_id": hero.id,
        "meal_id": meal.id,
        "message": "msg, please"
    }
    response = client.post("api/orders/", json=payload)
    # Assert sleep was called with the mocked sleep_time
    mock_sleep.assert_called_once_with(sleep_time)

    # Assert process_order_logic called with any session and correct order_id
    mock_process_logic.assert_called_once()
    args = mock_process_logic.call_args[0]
    assert response.status_code == 201
    data = response.get_json()['data']
    assert data["hero_id"] == hero.id
    assert data["meal_id"] == meal.id
    assert data["status"] == "PENDING"
    assert data["message"] == "msg, please"


def test_get_order(client, order):
    response = client.get(f"api/orders/{order.id}")
    assert response.status_code == 200
    data = response.get_json()['data']
    assert data["id"] == order.id
    assert data["hero_id"] == order.hero_id
    assert data["meal_id"] == order.meal_id
    assert data["status"] == order.status.value


def test_create_order_invalid(client):
    # Missing hero_id
    payload = {
        "meal_id": 1
    }
    response = client.post("api/orders/", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "hero_id" in data["errors"]

