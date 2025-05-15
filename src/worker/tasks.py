import time
import random
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from api.views.order_service import process_order_logic
from config import Config
from api.models import Order, Hero, Meal, OrderStatus


import logging

logger = logging.getLogger(__name__)


# separate flask session with the worker
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)

def process_order_task(order_id: int) -> None:
    logger.debug("order {order.id} is in queue")
    with SessionLocal() as session:
        try:
            time.sleep(random.uniform(1, 5))
            status = process_order_logic(session, order_id)
            logger.info("order {order.id} is in queue")
        except Exception as e:
            logger.info("order {order.id} failed :",e)
