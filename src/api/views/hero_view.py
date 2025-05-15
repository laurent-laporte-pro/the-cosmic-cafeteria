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
        GET /heroes/ or /heroes/<hero_id>
        """
        if hero_id is None:
            heroes = Hero.query.all()
            return success_response(heroes_schema.dump(heroes))

        hero = Hero.query.get_or_404(hero_id)
        return success_response(hero_schema.dump(hero))

    def post(self) -> Response:
        """
        POST /heroes/
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
        PUT /heroes/<hero_id>
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
        DELETE /heroes/<hero_id>
        """
        hero = Hero.query.get_or_404(hero_id)

        try:
            db.session.delete(hero)
            db.session.commit()
            return success_response(f"Hero '{hero.name}' deleted", 204)

        except SQLAlchemyError:
            db.session.rollback()
            return error_response("Database error", 500)
