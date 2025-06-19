import pytest
from flask import Flask
from flask_restful import Api

from app.main import db
from app.routes.hero import HeroesList
from database.sql_conf import SqliteTestConfig

# Sample hero JSON to use in POST
sample_hero_payload = {
    "name": "Test Hero",
    "suit_color": "Green",
    "has_cape": True,
    "is_retired": True,
    "last_mission": "2025-06-18T14:00:00.000Z",
    "powers": ["Flying", "Invisibility"]
}


@pytest.fixture
def test_client():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SqliteTestConfig.SQLALCHEMY_DATABASE_URI
    app.config[
        'SQLALCHEMY_TRACK_MODIFICATIONS'] = SqliteTestConfig.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['TESTING'] = True
    db.init_app(app)
    api = Api(app)
    api.add_resource(HeroesList, '/hero/')
    with app.app_context():
        db.create_all()
        client = app.test_client()
        yield client
        db.session.remove()
        db.drop_all()


def test_get_heroes_empty(test_client):
    # Arrange: Nothing to arrange, DB is empty

    # Act
    response = test_client.get('/hero/')

    # Assert
    assert response.status_code == 200
    assert response.get_json() == []


def test_post_new_hero(test_client):
    # Arrange
    payload = sample_hero_payload

    # Act
    response = test_client.post('/hero/', json=payload)
    data = response.get_json()

    # Assert
    assert response.status_code == 200
    assert data['name'] == payload['name']
    assert data['suit_color'] == payload['suit_color']
    assert data['has_cape'] == payload['has_cape']


def test_get_hero_with_filter(test_client):
    # Arrange
    test_client.post('/hero/', json=sample_hero_payload)

    # Act
    response = test_client.get('/hero/?suit_color=Green')
    data = response.get_json()

    # Assert
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['name'] == sample_hero_payload['name']


def test_get_hero_with_wrong_filter(test_client):
    # Arrange
    test_client.post('/hero/', json=sample_hero_payload)

    # Act
    response = test_client.get('/hero/?suit_color=Purple')
    data = response.get_json()

    # Assert
    assert response.status_code == 200
    assert data == []