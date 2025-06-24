from datetime import datetime
from flasgger import Swagger
from flask import Flask

from app.extension.celery.celery_app import celery_init_app
from database.models import db
from database.models.hero import Hero
from database.models.power import Power
from database.sql_conf import BaseSqlConfig

flask_app = Flask(__name__)

flask_app.config['SQLALCHEMY_DATABASE_URI'] = BaseSqlConfig.SQLALCHEMY_DATABASE_URL
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
flask_app.config["CELERY"] = {"broker_url": "redis://localhost:6379", "result_backend": "redis://localhost:6379"}
db.init_app(flask_app)
celery_init_app(flask_app)

with flask_app.app_context():
    # Create all tables defined in the models
    db.create_all()
    print("In-memory SQLite database and tables 'hero', 'power' created successfully.")

    print("Adding some sample data...")
    try:
        # Create sample heroes
        hero1 = Hero(name="Superman", suit_color="Blue", has_cape=True, last_mission=datetime(2023, 1, 15),
                     is_retired=False)
        hero2 = Hero(name="Batman", suit_color="Black", has_cape=True, last_mission=datetime(2024, 3, 10),
                     is_retired=False)
        hero3 = Hero(name="Wonder Woman", suit_color="Red", has_cape=True, last_mission=datetime(2023, 11, 5),
                     is_retired=False)

        db.session.add_all([hero1, hero2, hero3])
        db.session.commit()

        # Create sample powers linked to heroes
        power1 = Power(name="Flight", hero_id=hero1.id)
        power2 = Power(name="Super Strength", hero_id=hero1.id)
        power3 = Power(name="Gadgets", hero_id=hero2.id)
        power4 = Power(name="Tactical Genius", hero_id=hero2.id)
        power5 = Power(name="Super Strength", hero_id=hero3.id)
        power6 = Power(name="Lasso of Truth", hero_id=hero3.id)

        db.session.add_all([power1, power2, power3, power4, power5, power6])
        db.session.commit()
        print("Sample data added successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while adding sample data: {e}")
    finally:
        db.session.close()

swagger = Swagger(app=flask_app, template_file=None)
