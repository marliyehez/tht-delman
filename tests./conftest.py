import pytest
from project.app import create_app, db

@pytest.fixture()
def app():
    app = create_app('../tests/config_test.py')

    yield app
    
    with app.app_context():
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()
