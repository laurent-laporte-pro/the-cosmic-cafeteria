import time
import random
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from api.services.order_service import process_order_logic
from config.settings import settings

# todo -> update loggr for all files
logger = logging.getLogger(__name__)

# decoupling the worker from the flask App
engine = create_engine(settings.DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)

def process_order_task(order_id: int) -> None:
    with SessionLocal() as session:
        try:
            time.sleep(random.uniform(1, 5))
            status = process_order_logic(session, order_id)
            logger.info(f"Order {order_id} processed: {status}")
        except Exception as e:
            logger.exception(f"Failed to process order {order_id}: {e}")
