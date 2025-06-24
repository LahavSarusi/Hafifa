from flask_restful import Resource
from flask import request
from flasgger import swag_from

from app.decorators import commit_db
from app.extension.socket.socketio_manager import socketio
from database.services.hero_service import get_heroes, add_hero_with_his_powers, set_hero_is_retired, \
    set_hero_last_mission
from database.queries.hero_queries import get_hero_by_id
from app.schemas.hero import HeroFilters, NewHero, HeroSchema
from database.models import db


class HeroById(Resource):
    @swag_from('swagger_templates\hero\hero_by_id.yml')
    def get(self, id):
        hero = get_hero_by_id(hero_id=int(id))
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
        hero = set_hero_is_retired(hero_id=int(id))
        hero_to_json = HeroSchema.from_orm(hero).model_dump(mode='json')
        socketio.emit('hero_retired', hero_to_json)
        return hero_to_json


class UpdateHeroLastMission(Resource):
    @commit_db(db)
    @swag_from('swagger_templates/hero/update_hero_last_mission.yml')
    def put(self, id):
        """
        Updates a hero's last_mission attribute to a given timestamp.
        """
        timestamp_as_string = request.json['timestamp']
        hero = set_hero_last_mission(int(id), timestamp_as_string)
        return HeroSchema.from_orm(hero).model_dump(mode='json'), 200
