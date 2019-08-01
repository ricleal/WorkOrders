import pytest
from faker import Faker
from orders import create_app
from orders.config import TestingConfig
from orders import db

@pytest.fixture
def app():
    app = create_app(TestingConfig)
    app_context = app.test_request_context()
    app_context.push()
    db.create_all()

    yield app
    
    db.session.remove()
    db.drop_all()
    app_context.pop()


@pytest.fixture
def fake():
    f = Faker()
    #f.seed(123)
    return f
