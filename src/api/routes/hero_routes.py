from flask import Blueprint, request, jsonify
from api.extensions import db
from api.models.Hero import Hero
from api.schemas.hero_schema import HeroSchema
from sqlalchemy.exc import SQLAlchemyError

hero_blueprint = Blueprint("hero_blueprint", __name__, url_prefix="/heroes")  # Changed to plural "heroes"
hero_schema = HeroSchema()
heroes_schema = HeroSchema(many=True)



#------FETCH HEROS ---------#
@hero_blueprint.route('/', methods=['GET'])
def get_heroes():
    try:
        heroes = Hero.query.all()
        return heroes_schema.jsonify(heroes)
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500



#------FETCH HERO BY ID ---------#
@hero_blueprint.route('/<int:hero_id>', methods=['GET'])
def get_hero(hero_id):
    hero = Hero.query.get_or_404(hero_id, description=f"Hero with ID {hero_id} not found")
    return hero_schema.jsonify(hero)





#------CREATE A HERO ---------#
@hero_blueprint.route('/', methods=['POST'])
def create_hero():
    try:
        data = request.get_json()
        hero = hero_schema.load(data)
        db.session.add(hero)
        db.session.commit()
        return hero_schema.jsonify(hero), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400



#------UPDATE HERO : ALL INFO ---------#
@hero_blueprint.route('/<int:hero_id>', methods=['PUT'])
def update_hero(hero_id):
    try:
        hero = Hero.query.get_or_404(hero_id)
        data = request.get_json()
        
        hero_schema.load(data, instance=hero, partial=False)
        
        db.session.commit()
        return hero_schema.jsonify(hero)
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400





#------UPDATE HERO : partial ---------#
@hero_blueprint.route('/<int:hero_id>', methods=['PATCH'])
def partial_update_hero(hero_id):
    try:
        hero = Hero.query.get_or_404(hero_id)
        data = request.get_json()
        
        hero_schema.load(data, instance=hero, partial=True)
        
        db.session.commit()
        return hero_schema.jsonify(hero)
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400





#------DELETE HERO ---------#
@hero_blueprint.route('/<int:hero_id>', methods=['DELETE'])
def delete_hero(hero_id):
    try:
        hero = Hero.query.get_or_404(hero_id)
        db.session.delete(hero)
        db.session.commit()
        return jsonify({"message": f"Hero with ID {hero_id} deleted successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400