
from flask.views import MethodView
from flask import request
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from werkzeug.wrappers import Response

from api.app_extensions import db
from api.models.order import Order, OrderStatus
from api.models.hero import Hero
from api.models.meal import Meal
from api.schemas.order_schema import OrderSchema, OrderDeleteActionSchema
from api.views.utils import success_response, error_response
from jobs.queue import default_queue
from worker.tasks import process_order_task


import logging

logger = logging.getLogger(__name__)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)


class OrderAPI(MethodView):
    def get(self, order_id: int = None) -> Response:
        """
        Get one order or list all orders
        ---
        tags:
          - Orders
        parameters:
          - name: order_id
            in: path
            type: integer
            required: false
            description: ID of the order to fetch
        responses:
          200:
            description: A single order or list of orders
            schema:
              oneOf:
                - $ref: '#/api/orders'
                - type: array
                  items:
                    $ref: '#/api/orders'
          404:
            description: Order not found
        """
        if order_id is None:
            orders = Order.query.all()
            return success_response(orders_schema.dump(orders))

        order = Order.query.get_or_404(order_id)
        return success_response(order_schema.dump(order))

    def post(self) -> Response:
        """
        Create a new order
        ---
        tags:
          - Orders
        consumes:
          - application/json
        parameters:
          - in: body
            name: body
            required: true
            schema:
              $ref: '#/api/orders'
        responses:
          201:
            description: Order created and processing started
            schema:
              $ref: '#/api/orders'
          400:
            description: Validation error
          409:
            description: Invalid references
          500:
            description: Database or queue error
        """
        try:
            data: dict = request.get_json(force=True)
            order: Order = order_schema.load(data)
            # Get hero and meal
            hero = Hero.query.get_or_404(order.hero_id)
            meal = Meal.query.get_or_404(order.meal_id)

            # Save to DB
            db.session.add(order)
            db.session.commit()

            try:
                default_queue.enqueue(process_order_task, order.id)
                logger.debug("order {order.id} is processing")

            except Exception as e:
                logger.error("order {order.id} is failed in proceess")
                return {"error": "Failed to enqueue order processing"}, 500

            
            logger.info("order {order.id} sucessefuly processed")
            return success_response(order_schema.dump(order), 201)

        except ValidationError as err:
            logger.error("order {order.id} is failed in proceess")
            return error_response("Validation failed", 400, err.messages)

        except IntegrityError:
            db.session.rollback()
            logger.error("order {order.id} is failed in proceess")
            return error_response("Invalid references", 409)

        except SQLAlchemyError:
            db.session.rollback()
            logger.error("order {order.id} is failed in proceess")
            return error_response("Database error", 500)

    def delete(self, order_id: int) -> Response:
        """
        Cancel or delete an order
        ---
        tags:
          - Orders
        consumes:
          - application/json
        parameters:
          - name: order_id
            in: path
            type: integer
            required: true
            description: ID of the order to delete or cancel
          - in: body
            name: body
            schema:
              $ref: '#/api/orders'
        responses:
          200:
            description: Order canceled
          204:
            description: Order deleted
          400:
            description: Invalid action or state
          404:
            description: Order not found
        """
        try:
            data = OrderDeleteActionSchema().load(request.get_json(force=True) or {})
        except ValidationError as err:
            return error_response(err.messages, 400)

        action = data["action"]
        order = Order.query.get_or_404(order_id)

        if action == "cancel":
            if order.status in {OrderStatus.COMPLETED, OrderStatus.CANCELLED}:
                return error_response("Order cannot be canceled in its current state", 400)
            order.status = OrderStatus.CANCELLED
            db.session.commit()
            logger.warning("order {order.id} canceled")
            return success_response("canceled", 200)

        elif action == "delete":
            db.session.delete(order)
            db.session.commit()
            logger.warning("order {order.id} deleted")
            return success_response("deleted", 204)
