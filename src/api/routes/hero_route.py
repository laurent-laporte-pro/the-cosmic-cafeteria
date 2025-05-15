from flask import Blueprint
from api.views.hero_view import HeroAPI

hero_bp = Blueprint('hero', __name__)

hero_view = HeroAPI.as_view('hero_api')
hero_bp.add_url_rule('/heroes/', defaults={'hero_id': None}, view_func=hero_view, methods=['GET'])
hero_bp.add_url_rule('/heroes/', view_func=hero_view, methods=['POST'])
hero_bp.add_url_rule('/heroes/<int:hero_id>', view_func=hero_view, methods=['GET', 'PUT', 'DELETE'])
