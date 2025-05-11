import pytest
import time
from datetime import datetime
from redis import Redis
from rq import Queue
from src.api.models import Hero, Meal, Order, OrderStatus, db
from src.worker.tasks import process_order

# ---- Fixtures ----
@pytest.fixture
def redis_queue(app):
    q = Queue(connection=Redis.from_url(app.config['REDIS_URL']))
    q.empty()  # Clear queue before test
    yield q
    q.empty()  # Cleanup after test




def test_order_fulfillment_workflow(client, db, redis_queue):
    """Test complete happy path from order creation to fulfillment"""
    # 1. Create Hero and Meal
    hero = Hero(name="Workflow Hero", allergies=[])
    meal = Meal(name="Workflow Meal", ingredients=[])
    db.session.add_all([hero, meal])
    db.session.commit()

    # 2. Create Order via API
    response = client.post('/orders', json={
        "hero_id": hero.id,
        "meal_id": meal.id
    })
    assert response.status_code == 202
    order_id = response.json["id"]

    # 3. Verify job was queued
    assert redis_queue.count == 1
    job = redis_queue.jobs[0]
    assert job.func_name == 'worker.tasks.process_order'
    assert job.args[0] == order_id

    # 4. Process the job manually (simulating worker)
    job.perform()

    # 5. Verify final state
    order = Order.query.get(order_id)
    assert order.status == OrderStatus.COMPLETED
    assert order.processed_at is not None

def test_rejected_order_workflow(client, db, redis_queue):
    """Test order rejection due to allergies"""
    # allergic hero
    hero = Hero(name="Allergic Hero", allergies=["peanuts"])
    meal = Meal(name="Peanut Meal", ingredients=["peanuts"])
    db.session.add_all([hero, meal])
    db.session.commit()

    # Create order
    response = client.post('/orders', json={
        "hero_id": hero.id,
        "meal_id": meal.id
    })
    order_id = response.json["id"]

    # Process job
    redis_queue.jobs[0].perform()

    # Verify rejection
    order = Order.query.get(order_id)
    assert order.status == OrderStatus.CANCELLED
    assert "peanut" in order.message.lower()


