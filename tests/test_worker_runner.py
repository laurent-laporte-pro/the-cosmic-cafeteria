import time
import pytest
from rq import Worker
from jobs.queue import default_queue
from worker.tasks import process_order_task
from api.models import Hero, Meal, Order, OrderStatus
from unittest.mock import patch, MagicMock


# todo --> this test fail to be resolved 
def test_process_order_rq(session, order):
    from worker.tasks import process_order_task
    from jobs.queue import default_queue
    from rq import Worker

    session.commit()  # Ensure order is persisted
    print(f"Test order ID: {order.id}, Status: {order.status.name}")

    default_queue.empty()
    job = default_queue.enqueue(process_order_task, order.id)
    print(f"Enqueued job ID: {job.id}, Status: {job.get_status()}")
    assert job is not None
    assert job.get_status() == 'queued'

    worker = Worker([default_queue], connection=default_queue.connection)
    worker.work(burst=True)
    print(f"Job status after worker: {job.get_status()}")
    if job.get_status() == 'failed':
        print(f"Job failure reason: {job.exc_info}")

    session.commit()
    updated_order = session.get(Order, order.id)
    session.refresh(updated_order)
    print(f"Final order status: {updated_order.status.name}")
    assert updated_order.status.name in ("COMPLETED", "CANCELLED")