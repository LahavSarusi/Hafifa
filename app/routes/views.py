from flask_restful import Api

from .index import HealthCheck, CheckSocket
from .power import PowerByHeroId
from .hero import HeroById, HeroesList, RetireHero, UpdateHeroLastMission
from app import flask_app

api = Api(flask_app)

def add_api_resources():
    api.add_resource(HealthCheck, '/')
    api.add_resource(CheckSocket, '/test_socket')
    api.add_resource(HeroById, '/hero/<int:id>')
    api.add_resource(HeroesList, '/hero/')
    api.add_resource(RetireHero, '/hero/retire/<int:id>')
    api.add_resource(UpdateHeroLastMission, '/hero/last_mission/<int:id>')
    api.add_resource(PowerByHeroId, '/power/<int:hero_id>')
