from werkzeug.exceptions import NotFound

from database.models.power import Power
from database.models import db
from typing import List


def get_powers_by_hero_id(hero_id: int) -> List[Power]:
    """
    Get all powers by hero id.

    Query Parameters:
    - hero_id (str): Search the powers by their hero id
    """
    powers = Power.query.filter_by(hero_id=hero_id).all()
    if not powers:
        raise NotFound(f"Powers with hero ID {hero_id} not found.")
    return powers


def update_hero_powers(hero_id: int, new_power_names: List[str]) -> List[Power]:
    """
    Updates a hero's powers in the database.
    This function compares the existing powers of a hero with a new list of power names.
    Powers that present in the database but not in `new_power_names` will be removed.
    Power names in `new_power_names` that are not present in the database will be added.
    Existing powers that are also in `new_power_names` will be untouched.

    Query Parameters:
    - hero_id (int): The ID of the hero whose powers are to be updated.
    - new_power_names (List[str]): A list of power names that the hero should have after the update.
    """
    current_powers = get_powers_by_hero_id(hero_id)

    # Identify powers to remove
    for power in current_powers:
        if power.name not in new_power_names:
            db.session.delete(power)
            current_powers.remove(power)

    # Identify powers to add
    current_power_names = {power.name for power in current_powers}
    for name in new_power_names:
        if name not in current_power_names:
            new_power = Power(name=name, hero_id=hero_id)
            db.session.add(new_power)
            current_powers.append(new_power)

    db.session.flush()

    return current_powers