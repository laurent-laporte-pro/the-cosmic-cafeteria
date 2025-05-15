from flask.views import MethodView
from flask import request
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from marshmallow import ValidationError
from werkzeug.wrappers import Response

from api.app_extensions import db
from api.models.meal import Meal
from api.schemas.meal_schema import MealSchema
from api.views.utils import success_response, error_response

meal_schema = MealSchema()
meals_schema = MealSchema(many=True)


class MealAPI(MethodView):
    def get(self, meal_id: int = None) -> Response:
        """
        Get one meal by ID or list all meals
        ---
        tags:
          - Meals
        parameters:
          - name: meal_id
            in: path
            type: integer
            required: false
            description: ID of the meal to fetch
        responses:
          200:
            description: A single meal or list of meals
            schema:
              oneOf:
                - $ref: '#/api/meals'
                - type: array
                  items:
                    $ref: '#/api/meals'
          404:
            description: Meal not found
        """
        if meal_id is None:
            meals = Meal.query.all()
            return success_response(meals_schema.dump(meals))

        meal = Meal.query.get_or_404(meal_id)
        return success_response(meal_schema.dump(meal))

    def post(self) -> Response:
        """
        Create a new meal
        ---
        tags:
          - Meals
        consumes:
          - application/json
        parameters:
          - in: body
            name: body
            required: true
            schema:
              $ref: '#/api/meals'
        responses:
          201:
            description: Meal created successfully
            schema:
              $ref: '#/api/meals'
          400:
            description: Validation error
          409:
            description: Duplicate or invalid reference error
          500:
            description: Database error
        """
        try:
            data: dict = request.get_json(force=True)
            meal: Meal = meal_schema.load(data)
            db.session.add(meal)
            db.session.commit()
            return success_response(meal_schema.dump(meal), 201)

        except ValidationError as err:
            return error_response("Validation failed", 400, err.messages)

        except IntegrityError:
            db.session.rollback()
            return error_response("Duplicate or invalid reference", 409)

        except SQLAlchemyError:
            db.session.rollback()
            return error_response("Database error", 500)

    def put(self, meal_id: int) -> Response:
        """
        Update an existing meal
        ---
        tags:
          - Meals
        consumes:
          - application/json
        parameters:
          - name: meal_id
            in: path
            type: integer
            required: true
            description: ID of the meal to update
          - in: body
            name: body
            required: true
            schema:
              $ref: '#/api/meals'
        responses:
          200:
            description: Meal updated successfully
            schema:
              $ref: '#/api/meals'
          400:
            description: Validation error
          404:
            description: Meal not found
          500:
            description: Database error
        """
        meal = Meal.query.get_or_404(meal_id)

        try:
            data: dict = request.get_json(force=True)
            updated: Meal = meal_schema.load(data, instance=meal, partial=True)
            db.session.commit()
            return success_response(meal_schema.dump(updated))

        except ValidationError as err:
            return error_response("Validation failed", 400, err.messages)

        except SQLAlchemyError:
            db.session.rollback()
            return error_response("Database error", 500)

    def delete(self, meal_id: int) -> Response:
        """
        Delete a meal by ID
        ---
        tags:
          - Meals
        parameters:
          - name: meal_id
            in: path
            type: integer
            required: true
            description: ID of the meal to delete
        responses:
          204:
            description: Meal deleted successfully (No Content)
          404:
            description: Meal not found
          500:
            description: Database error
        """
        meal = Meal.query.get_or_404(meal_id)

        try:
            db.session.delete(meal)
            db.session.commit()
            return success_response(f"Meal '{meal.name}' deleted", 204)

        except SQLAlchemyError:
            db.session.rollback()
            return error_response("Database error", 500)
