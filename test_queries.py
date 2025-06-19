import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from datetime import datetime
import pytest
from werkzeug.exceptions import NotFound

from app.schemas.hero import HeroSchema
from database.models.hero import Hero
from database.models.power import Power
from database.queries.power_queries import get_powers_by_hero_id
from database.queries.hero_queries import get_hero_by_id, get_heroes_by_filters, add_hero_with_powers
from database.sql_conf import SqliteTestConfig
from app.main import db


class TestHeroPower(unittest.TestCase):

    def setUp(self):
        # Create a new Flask application instance for testing and configure the application to use an in-memory SQLite database
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = SqliteTestConfig.SQLALCHEMY_DATABASE_URI
        self.app.config[
            'SQLALCHEMY_TRACK_MODIFICATIONS'] = SqliteTestConfig.SQLALCHEMY_TRACK_MODIFICATIONS  # Disable it to improve performance
        db.init_app(self.app)

        # Create and push a new application context to manage the database connection
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create all tables in the database
        db.create_all()

        # Adding heroes and powers to the sqlite test db
        hero1 = Hero(id=1, name='Test Hero 1', suit_color='Red', has_cape=True, last_mission=datetime.now(),
                     is_retired=False)
        hero2 = Hero(id=2, name='Test Hero 2', suit_color='Blue', has_cape=False, last_mission=datetime.now(),
                     is_retired=False)
        hero3 = Hero(id=3, name='Test Hero 3', suit_color='Yellow', has_cape=False, last_mission=datetime.now(),
                     is_retired=False)

        power1 = Power(hero_id=hero1.id, name='Power 1')
        power2 = Power(hero_id=hero1.id, name='Power 2')
        db.session.add_all([hero1, hero2, hero3, power1, power2])
        db.session.commit()

    def tearDown(self):
        # Remove the current database session to prevent interference with subsequent tests
        db.session.remove()
        # Drop all tables in the database to clear any test data
        db.drop_all()
        # Pop the current application context to ensure a clean slate for future tests
        self.app_context.pop()

    def test_get_hero_by_id_found(self):
        # Arrange: Setup the test data
        hero_id = 1

        # Act: Get the hero by id
        retrieved_hero = get_hero_by_id(hero_id)

        # Assert: Verify the hero is found by id
        assert retrieved_hero.id == 1

    def test_get_hero_by_id_not_found(self):
        # Arrange
        hero_id = 999

        # Act + Assert: Get a hero by non-existent id
        with pytest.raises(NotFound) as exc_info:
            get_hero_by_id(hero_id)

        # Assert: Verify the hero is not found by id
        assert f"Hero with ID {hero_id} not found." in str(exc_info.value)

    def test_get_heroes_by_filters_name(self):
        # Arrange: Setup the test data
        filter_name = "Test Hero"

        # Act: Query heroes by name filter
        result = get_heroes_by_filters(name=filter_name)

        # Assert: Verify the heroes are found by name filter
        assert len(result) == 3
        for hero in result:
            assert "Test Hero" in hero.name

    def test_get_heroes_by_filters_suit_color(self):
        # Arrange: Setup the test data
        filter_suit_color = "Red"

        # Act: Query the heroes by suit color filter
        result = get_heroes_by_filters(suit_color=filter_suit_color)

        # Assert: Verify the heroes are found by suit color filter
        assert len(result) == 1
        assert result[0].suit_color == filter_suit_color

    def test_get_heroes_by_filters_has_cape(self):
        # Arrange: Setup the test data
        filter_has_cape = True

        # Act: Query the heroes by cape filter
        result = get_heroes_by_filters(has_cape=filter_has_cape)

        # Assert: Verify the heroes are found by cape filter
        assert len(result) == 1
        assert result[0].has_cape == filter_has_cape

    def test_get_heroes_by_filters_all_filters(self):
        # Arrange: Setup the test data
        filter_name = "Test Hero"
        filter_suit_color = "Red"
        filter_has_cape = True

        # Act: Query heroes by all filters
        result = get_heroes_by_filters(name=filter_name, suit_color=filter_suit_color, has_cape=filter_has_cape)

        # Assert: Verify the heroes are found by all filters
        assert len(result) == 1
        assert "Test Hero" in result[0].name
        assert result[0].suit_color == "Red"
        assert result[0].has_cape

    def test_get_powers_by_hero_id_found(self):
        # Arrange: Setup the test data
        hero_id = 1

        # Act: Query powers by hero id
        result = get_powers_by_hero_id(hero_id)

        # Assert: Verify the powers are found by hero id
        assert len(result) == 2

    def test_get_powers_by_hero_id_not_found(self):
        # Arrange: Setup the test data
        hero_id = 999

        # Act + Assert: Query powers by non-existent hero id
        with pytest.raises(NotFound) as exc_info:
            get_powers_by_hero_id(hero_id)

        # Assert: Verify the powers are not found by hero id
        assert f"Powers with hero ID {hero_id} not found." in str(exc_info.value)

    def test_add_hero_with_powers_success(self):
        # Arrange: Setup the test data
        new_hero = HeroSchema(name="Test Hero", suit_color="Green", has_cape=False, last_mission=datetime.now(),
                              is_retired=False)
        hero_powers = ["Power 1", "Power 2"]

        # Act: Add the hero with powers
        result = add_hero_with_powers(new_hero.model_dump(), hero_powers)

        # Assert: Verify the hero is added successfully
        assert result.name == new_hero.name
        assert result.suit_color == new_hero.suit_color
        assert result.has_cape == new_hero.has_cape
        assert result.last_mission is not None
        assert result.is_retired == new_hero.is_retired

        # Assert: Verify the powers are added successfully
        result_powers = get_powers_by_hero_id(result.id)
        assert len(result_powers) == 2
        assert result_powers[0].name == hero_powers[0]
        assert result_powers[1].name == hero_powers[1]

    @patch('database.queries.hero_queries.Hero')
    def test_get_hero_by_id_raise_exception(self, mock_hero_class):
        # Arrange: Simulate an error when querying a hero by id
        mock_query = MagicMock()
        mock_query.get.side_effect = Exception("Database error")
        mock_hero_class.query = mock_query
        hero_id = 1

        # Act and Assert: Verify the exception is raised when getting the hero by id
        with pytest.raises(Exception) as exc_info:
            get_hero_by_id(hero_id)
        assert str(exc_info.value) == "Database error"

    @patch('database.queries.hero_queries.Hero')
    def test_get_heroes_by_filters_raise_exception(self, mock_hero_class):
        # Arrange: Simulate an error when querying heroes by filters
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.filter_by.return_value = mock_query
        mock_query.all.side_effect = Exception("Database error")
        mock_hero_class.query = mock_query

        # Act and Assert: Verify the exception is raised when getting the heroes by filters
        with pytest.raises(Exception) as exc_info:
            get_heroes_by_filters()
        assert str(exc_info.value) == "Database error"

    @patch('database.queries.power_queries.Power')
    def test_get_powers_by_hero_id_error(self, mock_power_class):
        # Arrange: Simulate an error when querying powers by hero id
        mock_query = MagicMock()
        mock_query.filter_by.return_value = mock_query
        mock_query.all.side_effect = Exception("Database error")
        mock_power_class.query = mock_query
        hero_id = 1

        # Act and Assert: Verify the exception is raised when getting the powers by hero id
        with pytest.raises(Exception) as exc_info:
            get_powers_by_hero_id(hero_id)
        assert str(exc_info.value) == "Database error"

    @patch('database.queries.hero_queries.db')
    def test_add_hero_with_powers_raise_exception(self, mock_hero_class):
        # Arrange: Simulate an error when creating a hero
        mock_query = MagicMock()
        mock_query.add.side_effect = Exception("Database error")
        mock_hero_class.session = mock_query

        new_hero = HeroSchema(name="Test Hero", suit_color="Green", has_cape=False, last_mission=datetime.now(),
                              is_retired=False).model_dump()
        hero_powers = ["Power 1", "Power 2"]

        # Act and Assert: Verify the exception is raised when creating the hero
        with pytest.raises(Exception) as exc_info:
            add_hero_with_powers(new_hero, hero_powers)
        assert str(exc_info.value) == "Database error"


if __name__ == '__main__':
    unittest.main()
