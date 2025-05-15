from flask import Blueprint
from api.views.meal_view import MealAPI

meal_bp = Blueprint('meal', __name__)

meal_view = MealAPI.as_view('meal_api')
meal_bp.add_url_rule('/meals/', defaults={'meal_id': None}, view_func=meal_view, methods=['GET'])
meal_bp.add_url_rule('/meals/', view_func=meal_view, methods=['POST'])
meal_bp.add_url_rule('/meals/<int:meal_id>', view_func=meal_view, methods=['GET', 'PUT', 'DELETE'])
