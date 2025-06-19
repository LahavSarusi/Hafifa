from werkzeug.exceptions import NotFound

from database.models import db
from database.models.hero import Hero
from database.models.power import Power
from typing import List, Optional, Dict


def get_hero_by_id(hero_id: int) -> Optional[Hero]:
    """
    Get hero by id

    Query Parameters:
    - hero_id (int): Search a hero with the id
    """
    hero = Hero.query.get(hero_id)
    if not hero:
        raise NotFound(f"Hero with ID {hero_id} not found.")
    return hero


def get_heroes_by_filters(name: Optional[str] = None, suit_color: Optional[str] = None,
                          has_cape: Optional[bool] = None) -> List[Hero]:
    """
    Get all heroes by filters.

    Query Parameters:
    - suit_color (str): Filter heroes by suit color
    - has_cape (bool): Filter heroes by cape presence
    - name (str): Filter heroes by name (Like)
    """
    query = Hero.query
    if name:
        query = query.filter(Hero.name.like(f"%{name}%"))
    if suit_color:
        query = query.filter_by(suit_color=suit_color)
    if has_cape is not None:
        query = query.filter_by(has_cape=has_cape)
    heroes = query.all()
    return heroes


def add_hero_with_powers(new_hero: Dict, hero_powers: List) -> Hero:
    """
    Add a hero with his powers.

    Query Parameters:
    - new_hero: Dict
    - hero_powers: List
    """
    hero = Hero(**new_hero)
    db.session.add(hero)
    db.session.flush()  # Now I have the hero id

    all_powers = []
    for power_name in hero_powers:
        all_powers.append(Power(hero_id=hero.id, name=power_name))
    db.session.add_all(all_powers)

    return hero
