from typing import Any, List, Optional
from app.schemas.hero import HeroSchema, NewHero
from database.hero_queries import get_heroes_by_filters, add_hero_with_powers


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
