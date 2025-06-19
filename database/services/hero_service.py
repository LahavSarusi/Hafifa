from datetime import datetime
from typing import Any, List, Optional
from app.schemas.hero import HeroSchema, NewHero
from database.queries.hero_queries import get_heroes_by_filters, add_hero_with_powers, get_hero_by_id
from database.models.hero import Hero


def get_heroes(name: Optional[str] = None, suit_color: Optional[str] = None, has_cape: Optional[bool] = None) -> List[dict[str, Any]]:
    """
    Get all heroes by filters.

    Query Parameters:
    - suit_color (str): Filter heroes by suit color
    - has_cape (bool): Filter heroes by cape presence
    - name (str): Filter heroes by name (Like)
    """
    heroes = get_heroes_by_filters(name=name, suit_color=suit_color, has_cape=has_cape)
    return [HeroSchema.from_orm(hero).model_dump(mode='json') for hero in heroes]


def add_hero_with_his_powers(new_hero: NewHero) -> dict[str, Any]:
    """
    Add a hero.

    Query Parameters:
    - new_hero: NewHero
    """
    hero_dict = new_hero.model_dump()
    powers = hero_dict.pop('powers')
    hero = add_hero_with_powers(hero_dict, powers)
    return HeroSchema.from_orm(hero).model_dump(mode='json')


def set_hero_is_retired(hero_id: int) -> Optional[Hero]:
    """
    If the hero exists, is_retired field sets to True.

    Query Parameters:
    - hero_id: int
    """
    hero = get_hero_by_id(hero_id=int(hero_id))
    hero.is_retired = True
    return hero

def set_hero_last_mission(hero_id: int, timestamp_as_string: str) -> Optional[Hero]:
    """
    If the hero exists, last_mission field sets to the given timestamp.

    Query Parameters:
    - hero_id: int
    - timestamp_as_string: str
    """
    hero = get_hero_by_id(hero_id=hero_id)
    timestamp_as_datetime = datetime.strptime(timestamp_as_string, '%Y-%m-%dT%H:%M:%S.%fZ')
    hero.last_mission = timestamp_as_datetime
    return hero