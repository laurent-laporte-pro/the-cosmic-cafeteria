from flask import Blueprint, request, jsonify , current_app
from api.extensions import db
from api.models.Meal import Meal
from api.schemas.meal_schema import MealSchema
from sqlalchemy.exc import SQLAlchemyError

meal_blueprint = Blueprint("meal_blueprint", __name__, url_prefix="/meals")
meal_schema = MealSchema()
meals_schema = MealSchema(many=True)


#-------FETCH ALL MEALS --------#
@meal_blueprint.route('/', methods=['GET'])
def get_meals():
    try:
        current_app.logger.info(f"getting all meals ....")

        meals = Meal.query.all()
        return meals_schema.jsonify(meals)
    except SQLAlchemyError as e:
        current_app.logger.error(f"an error has occured while getting the meals ---> {str(e)}")

        return jsonify({"error": str(e)}), 500

#-------FETCH MEAL BY ID --------#
@meal_blueprint.route('/<int:meal_id>', methods=['GET'])
def get_meal(meal_id):
    current_app.logger.info(f"getting meal with id #{meal_id} ....")

    meal = Meal.query.get_or_404(meal_id, description=f"Meal with ID {meal_id} not found")
    return meal_schema.jsonify(meal)

#-------CREATE A NEW MEALS --------#
@meal_blueprint.route('/', methods=['POST'])
def create_meal():
    try:
        data = request.get_json()
        current_app.logger.info(f"creating a meal .........")

        if not all(key in data for key in ['name', 'ingredients', 'price', 'origin_planet']):
            current_app.logger.error(f"Meal Creation : an error has occured")

            return jsonify({"error": "Missing required fields"}), 400
            
        meal = meal_schema.load(data)
        db.session.add(meal)
        db.session.commit()
        current_app.logger.info(f"Meal Creation : meal created successfuly")

        return meal_schema.jsonify(meal), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

#-------UPDATE THE WHOLE MEAL --------#
@meal_blueprint.route('/<int:meal_id>', methods=['PUT'])
def update_meal(meal_id):
    try:
        meal = Meal.query.get_or_404(meal_id)
        data = request.get_json()
        current_app.logger.info(f"Updating the meal #{meal_id}")

        if not all(key in data for key in ['name', 'ingredients', 'price', 'origin_planet']):
            current_app.logger.info(f"an error has occured while updating the meal : missing info this is a put method")

            return jsonify({"error": "Missing required fields for full update"}), 400
            
        meal_schema.load(data, instance=meal, partial=False)
        db.session.commit()
        current_app.logger.info(f"Meal #{meal_id} updated succesffily")

        return meal_schema.jsonify(meal)
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

#-------UPDATE MEAL PARITALY --------#
@meal_blueprint.route('/<int:meal_id>', methods=['PATCH'])
def partial_update_meal(meal_id):
    try:
        meal = Meal.query.get_or_404(meal_id)
        data = request.get_json()
        current_app.logger.info(f"Updating meal #{meal_id} partialy")

        # No required fields check for partial update
        meal_schema.load(data, instance=meal, partial=True)
        db.session.commit()
        current_app.logger.info(f"meal #{meal_id} Updated partialy")

        return meal_schema.jsonify(meal)
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"an error has occured while Updating meal #{meal_id} , {str(e)} ")

        return jsonify({"error": str(e)}), 400

#-------DELETE A MEAL --------#
@meal_blueprint.route('/<int:meal_id>', methods=['DELETE'])
def delete_meal(meal_id):
    try:
        meal = Meal.query.get_or_404(meal_id)
        current_app.logger.info(f"Deleting the meal #{meal_id}")

        # CHECK IF THERE IS AN ORDER WITH THIS MEAL
        if meal.ordered_by:
            return jsonify({
                "error": "Cannot delete meal with existing orders",
                "solution": "Delete associated orders first or set them to another meal"
            }), 400
            
        db.session.delete(meal)
        db.session.commit()
        current_app.logger.info(f"meal #{meal_id} Deleted")

        return jsonify({"message": f"Meal with ID {meal_id} deleted successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"an error has occured while deleting the meal #{meal_id} , {str(e)}")

        return jsonify({"error": str(e)}), 400