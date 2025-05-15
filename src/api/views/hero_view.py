from flask.views import MethodView
from flask import request
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from marshmallow import ValidationError
from werkzeug.wrappers import Response

from api.app_extensions import db
from api.models.hero import Hero
from api.schemas.hero_schema import HeroSchema
from api.views.utils import success_response, error_response

hero_schema = HeroSchema()
heroes_schema = HeroSchema(many=True)


class HeroAPI(MethodView):
    def get(self, hero_id: int = None) -> Response:
        """
        Get one hero by ID or list all heroes
        ---
        tags:
          - Heroes
        parameters:
          - name: hero_id
            in: path
            type: integer
            required: false
            description: ID of the hero to fetch
        responses:
          200:
            description: A single hero or list of heroes
            schema:
              oneOf:
                - $ref: '#/api/heros'
                - type: array
                  items:
                    $ref: '#/api/heros'
          404:
            description: Hero not found
        """
        if hero_id is None:
            heroes = Hero.query.all()
            return success_response(heroes_schema.dump(heroes))

        hero = Hero.query.get_or_404(hero_id)
        return success_response(hero_schema.dump(hero))

    def post(self) -> Response:
        """
        Create a new hero
        ---
        tags:
          - Heroes
        consumes:
          - application/json
        parameters:
          - in: body
            name: body
            required: true
            schema:
              $ref: '#/api/heros'
        responses:
          201:
            description: Hero created successfully
            schema:
              $ref: '#/api/heros'
          400:
            description: Validation error
          409:
            description: Duplicate or invalid reference error
          500:
            description: Database error
        """
        try:
            data: dict = request.get_json(force=True)
            hero: Hero = hero_schema.load(data)
            db.session.add(hero)
            db.session.commit()
            return success_response(hero_schema.dump(hero), 201)

        except ValidationError as err:
            return error_response("Validation failed", 400, err.messages)

        except IntegrityError:
            db.session.rollback()
            return error_response("Duplicate or invalid reference", 409)

        except SQLAlchemyError as e:
            db.session.rollback()
            return error_response("Database error", 500)

    def put(self, hero_id: int) -> Response:
        """
        Update an existing hero
        ---
        tags:
          - Heroes
        consumes:
          - application/json
        parameters:
          - name: hero_id
            in: path
            type: integer
            required: true
            description: ID of the hero to update
          - in: body
            name: body
            required: true
            schema:
              $ref: '#/api/heros'
        responses:
          200:
            description: Hero updated successfully
            schema:
              $ref: '#/api/heros'
          400:
            description: Validation error
          404:
            description: Hero not found
          500:
            description: Database error
        """
        hero = Hero.query.get_or_404(hero_id)

        try:
            data: dict = request.get_json(force=True)
            updated: Hero = hero_schema.load(data, instance=hero, partial=True)
            db.session.commit()
            return success_response(hero_schema.dump(updated))

        except ValidationError as err:
            return error_response("Validation failed", 400, err.messages)

        except SQLAlchemyError:
            db.session.rollback()
            return error_response("Database error", 500)

    def delete(self, hero_id: int) -> Response:
        """
        Delete a hero by ID
        ---
        tags:
          - Heroes
        parameters:
          - name: hero_id
            in: path
            type: integer
            required: true
            description: ID of the hero to delete
        responses:
          204:
            description: Hero deleted successfully (No Content)
          404:
            description: Hero not found
          500:
            description: Database error
        """
        hero = Hero.query.get_or_404(hero_id)

        try:
            db.session.delete(hero)
            db.session.commit()
            return success_response(f"Hero '{hero.name}' deleted", 204)

        except SQLAlchemyError:
            db.session.rollback()
            return error_response("Database error", 500)
