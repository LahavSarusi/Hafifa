import requests
import os
from celery import shared_task
from datetime import datetime, timedelta
from database.models.hero import Hero
from database.models import db

BASE_API_URL = os.getenv("FLASK_API_URL", "http://localhost:5000")


@shared_task
def trigger_retire_hero(hero_id):
    url = f"{BASE_API_URL}/hero/retire/{hero_id}"
    try:
        response = requests.put(url)
        response.raise_for_status()
        return {
            "status": "success",
            "hero_id": hero_id,
            "response": response.json()
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "hero_id": hero_id,
            "error": str(e)
        }


@shared_task
def auto_retire_inactive_heroes():
    count = 0
    now = datetime.utcnow()
    cutoff = now - timedelta(hours=24)

    inactive_heroes = db.session.query(Hero).filter_by(is_retired=False).all()
    for hero in inactive_heroes:
        if hero.last_mission < cutoff:
            trigger_retire_hero.delay(hero.id)
            count += 1

    return {"status": "complete", "retired_count": count}
