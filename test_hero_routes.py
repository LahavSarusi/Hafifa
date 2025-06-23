from flask import Flask
from flask_restful import Api

from database.models import db
from app.routes.hero import HeroesList
from database.sql_conf import SqliteTestConfig


class TestHeroRoutes:
    @classmethod
    def setup_class(cls):
        cls.app = Flask(__name__)
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = SqliteTestConfig.SQLALCHEMY_DATABASE_URI
        cls.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SqliteTestConfig.SQLALCHEMY_TRACK_MODIFICATIONS
        cls.app.config['TESTING'] = True

        db.init_app(cls.app)
        api = Api(cls.app)
        api.add_resource(HeroesList, '/hero/')

        with cls.app.app_context():
            db.create_all()

        cls.client = cls.app.test_client()

    def setup_method(self):
        """Run before each test: clean up all data."""
        with self.app.app_context():
            meta = db.metadata
            for table in reversed(meta.sorted_tables):
                db.session.execute(table.delete())
            db.session.commit()

    @classmethod
    def teardown_class(cls):
        with cls.app.app_context():
            db.session.remove()

    @staticmethod
    def create_hero_payload(name="Test Hero", suit_color="Green", has_cape=True, is_retired=False,
                            last_mission="2025-06-18T14:00:00.000Z", powers=None):
        return {
            "name": name,
            "suit_color": suit_color,
            "has_cape": has_cape,
            "is_retired": is_retired,
            "last_mission": last_mission,
            "powers": powers or ["Flying", "Invisibility"]
        }

    def test_get_heroes_empty(self):
        # Arrange: Nothing to arrange, DB is empty

        # Act
        response = self.client.get('/hero/')

        # Assert
        assert response.status_code == 200
        assert response.get_json() == []

    def test_post_new_hero(self):
        # Arrange
        sample_hero_payload = self.create_hero_payload()

        # Act
        response = self.client.post('/hero/', json=sample_hero_payload)
        data = response.get_json()

        # Assert
        assert response.status_code == 200
        assert data['name'] == sample_hero_payload['name']
        assert data['suit_color'] == sample_hero_payload['suit_color']
        assert data['has_cape'] == sample_hero_payload['has_cape']

    def test_get_hero_with_filter(self):
        # Arrange
        sample_hero_payload = self.create_hero_payload()
        self.client.post('/hero/', json=sample_hero_payload)

        # Act
        response = self.client.get('/hero/?suit_color=Green')
        data = response.get_json()

        # Assert
        assert response.status_code == 200
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]['name'] == sample_hero_payload['name']

    def test_get_hero_with_wrong_filter(self):
        # Arrange
        sample_hero_payload = self.create_hero_payload()
        self.client.post('/hero/', json=sample_hero_payload)

        # Act
        response = self.client.get('/hero/?suit_color=Purple')
        data = response.get_json()

        # Assert
        assert response.status_code == 200
        assert data == []
