from flask import Flask
import requests
from database.sql_conf import SqliteTestConfig
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
from app.extension.celery.deployer import trigger_retire_hero, auto_retire_inactive_heroes, BASE_API_URL
from database.models.hero import Hero
from database.models import db



class TestDeployerTasks:
    @classmethod
    def setup_class(cls):
        cls.app = Flask(__name__)
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = SqliteTestConfig.SQLALCHEMY_DATABASE_URI
        cls.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SqliteTestConfig.SQLALCHEMY_TRACK_MODIFICATIONS
        cls.app.config['TESTING'] = True
        db.init_app(cls.app)

        with cls.app.app_context():
            db.create_all()

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

    @patch('requests.put')
    def test_trigger_retire_hero_success(self, mock_put):
        # Arrange
        expected_response = {"message": "Hero retired successfully"}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response
        mock_put.return_value = mock_response
        hero_id = 1

        # Act
        result = trigger_retire_hero(hero_id)

        # Assert
        mock_put.assert_called_once_with(f"{BASE_API_URL}/hero/retire/{hero_id}")
        assert result["status"] == "success"
        assert result["hero_id"] == hero_id
        assert result["response"] == expected_response

    @patch('requests.put')
    def test_trigger_retire_hero_error(self, mock_put):
        # Arrange
        mock_put.side_effect = requests.exceptions.RequestException("Connection refused")
        hero_id = 456

        # Act
        result = trigger_retire_hero(hero_id)

        # Assert
        mock_put.assert_called_once_with(f"{BASE_API_URL}/hero/retire/{hero_id}")
        assert result["status"] == "error"
        assert result["hero_id"] == hero_id
        assert "Connection refused" in result["error"]

    @patch('database.models.db.session')
    def test_auto_retire_inactive_heroes_no_inactive(self, mock_db_session):
        # Arrange
        mock_db_session.query.return_value.filter_by.return_value.all.return_value = []
        status = "complete"
        retired_count = 0

        # Act
        result = auto_retire_inactive_heroes()

        # Assert
        mock_db_session.query.assert_called_once_with(Hero)
        assert result["status"] == status
        assert result["retired_count"] == retired_count

    @patch('database.models.db.session')
    def test_auto_retire_inactive_heroes_some_inactive(self, mock_db_session):
        """
        Test auto_retire_inactive_heroes with a mix of active and inactive heroes.
        """
        # Arrange
        now = datetime.utcnow()
        status = "complete"
        retired_count = 2
        inactive_hero = Hero(id=1, name='Test Hero 1', suit_color='Red', has_cape=True,
                             last_mission=now - timedelta(hours=25), is_retired=False)
        active_hero = Hero(id=2, name='Test Hero 2', suit_color='Blue', has_cape=True,
                           last_mission=now - timedelta(hours=10), is_retired=False)
        retired_hero = Hero(id=3, name='Test Hero 3', suit_color='Yellow', has_cape=True,
                            last_mission=now - timedelta(hours=30), is_retired=False)
        mock_db_session.query.return_value.filter_by.return_value.all.return_value = [
            inactive_hero, active_hero, retired_hero
        ]

        # Act
        result = auto_retire_inactive_heroes()

        # Assert
        mock_db_session.query.assert_called_once_with(Hero)
        assert result["status"] == status
        assert result["retired_count"] == retired_count
