from flask_restful import Resource
from flasgger import swag_from
from flask import request

from app.decorators import commit_db
from app.schemas.power import PowerSchema
from database.hero_queries import get_hero_by_id
from database.power_queries import get_powers_by_hero_id, update_hero_powers
from database.models import db


class PowerByHeroId(Resource):
    @swag_from('swagger_templates/power/power_by_hero_id.yml')
    def get(self, hero_id):
        """
        Get powers by hero id
        """
        powers = get_powers_by_hero_id(hero_id=hero_id)
        if not powers:
            return {'error': 'Power not found'}, 404
        return [PowerSchema.from_orm(power).model_dump() for power in powers]

    @commit_db(db)
    @swag_from('swagger_templates/power/update_hero_powers.yml')
    def put(self, hero_id):
        """
        Update a hero's powers based on the provided list.
        """
        # Check if the hero exists
        hero = get_hero_by_id(hero_id=int(hero_id))
        if not hero:
            return {'error': 'Hero not found'}, 404

        updated_powers = update_hero_powers(hero_id=int(hero_id), new_power_names=request.json['powers'])
        return [PowerSchema.from_orm(power).model_dump() for power in updated_powers]
