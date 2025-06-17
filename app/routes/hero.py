from datetime import datetime

from flask_restful import Resource
from flask import request
from flasgger import swag_from

from app.decorators import commit_db
from database.functions import get_heroes, add_hero_with_his_powers
from database.hero_queries import get_hero_by_id
from app.schemas.hero import HeroFilters, NewHero, HeroSchema
from database.models import db


class HeroById(Resource):
    @swag_from('swagger_templates\hero\hero_by_id.yml')
    def get(self, id):
        hero = get_hero_by_id(hero_id=int(id))
        if not hero:
            return {'error': 'Hero not found'}, 404
        return HeroSchema.from_orm(hero).model_dump(mode='json')


class HeroesList(Resource):
    @swag_from('swagger_templates\hero\heroes_list.yml')
    def get(self):
        params = HeroFilters(**request.args.to_dict())
        heroes = get_heroes(
            name=params.name,
            suit_color=params.suit_color,
            has_cape=params.has_cape
        )
        return heroes

    @commit_db(db)
    @swag_from('swagger_templates\hero\hero_add.yml')
    def post(self):
        hero_data = NewHero(**request.json)
        new_hero = add_hero_with_his_powers(hero_data)
        return new_hero


class RetireHero(Resource):
    @commit_db(db)
    @swag_from('swagger_templates\hero\hero_retire.yml')
    def put(self, id):
        """
        Retire a hero by setting his is_retired field to True.
        """
        # Check if the hero exists
        hero = get_hero_by_id(hero_id=int(id))
        if not hero:
            return {'error': 'Hero not found'}, 404

        hero.is_retired = True
        return HeroSchema.from_orm(hero).model_dump(mode='json'), 200


class UpdateHeroLastMission(Resource):
    @commit_db(db)
    @swag_from('swagger_templates/hero/update_hero_last_mission.yml') 
    def put(self, id):
        """
        Updates a hero's last_mission attribute to a given timestamp.
        """
        # Check if the hero exists
        hero = get_hero_by_id(hero_id=int(id))
        if not hero:
            return {'error': 'Hero not found'}, 404

        timestamp_as_string = request.json['timestamp']
        timestamp_as_datetime = datetime.strptime(timestamp_as_string, '%Y-%m-%dT%H:%M:%S.%fZ')
        hero.last_mission = timestamp_as_datetime

        return HeroSchema.from_orm(hero).model_dump(mode='json'), 200
