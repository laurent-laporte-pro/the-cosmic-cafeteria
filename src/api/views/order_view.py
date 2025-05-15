
from flask.views import MethodView
from flask import request
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from werkzeug.wrappers import Response

from api.app_extensions import db
from api.models.order import Order, OrderStatus
from api.models.hero import Hero
from api.models.meal import Meal
from api.schemas.order_schema import OrderSchema
from api.utils import success_response, error_response
from jobs.queue import default_queue


order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)


class OrderAPI(MethodView):
    def get(self, order_id: int = None) -> Response:
        """
        GET /orders/ or /orders/<order_id>
        """
        if order_id is None:
            orders = Order.query.all()
            return success_response(orders_schema.dump(orders))

        order = Order.query.get_or_404(order_id)
        return success_response(order_schema.dump(order))

    def post(self) -> Response:
        """
        POST /orders/
        """
        try:
            data: dict = request.get_json(force=True)
            order: Order = order_schema.load(data)

            # Get hero and meal
            hero = Hero.query.get_or_404(order.hero_id)
            meal = Meal.query.get_or_404(order.meal_id)

            # Allergy check
            allergen_conflicts = set(hero.allergies).intersection(meal.ingredients)
            if allergen_conflicts:
                return error_response(
                    f"Order cannot be created. Hero is allergic to: {', '.join(allergen_conflicts)}", 
                    400
                )

            # Save to DB
            db.session.add(order)
            db.session.commit()

            try:
                default_queue.enqueue(process_order_task, new_order.id)
            except Exception as e:
                return {"error": "Failed to enqueue order processing"}, HTTPStatus.INTERNAL_SERVER_ERROR


            return success_response(order_schema.dump(order), 201)

        except ValidationError as err:
            return error_response("Validation failed", 400, err.messages)

        except IntegrityError:
            db.session.rollback()
            return error_response("Invalid references", 409)

        except SQLAlchemyError:
            db.session.rollback()
            return error_response("Database error", 500)

    def put(self, order_id: int) -> Response:
        """
        PUT /orders/<order_id>
        Update status or message
        """
        order = Order.query.get_or_404(order_id)
        data = request.get_json(force=True)

        try:
            status = data.get("status")
            message = data.get("message")

            if status and status not in OrderStatus._member_names_:
                return error_response("Invalid status", 400)

            if status:
                order.status = OrderStatus[status]
            if message:
                order.message = message

            db.session.commit()
            return success_response(order_schema.dump(order))

        except SQLAlchemyError:
            db.session.rollback()
            return error_response("Database error", 500)

    def delete(self, order_id: int) -> Response:
        """
        DELETE /orders/<order_id>
        """
        order = Order.query.get_or_404(order_id)
        try:
            db.session.delete(order)
            db.session.commit()
            return success_response(f"Order #{order.id} deleted", 204)
        except SQLAlchemyError:
            db.session.rollback()
            return error_response("Database error", 500)

    def _process_order_async(self, order_id: int) -> None:
        """
        Simulates order processing in background (replaceable with Celery task).
        """
        # In real apps: enqueue job to Celery/RQ
        order = Order.query.get(order_id)
        if order:
            order.status = OrderStatus.PROCESSING
            db.session.commit()
