import pytest
from faker import Faker
from faker.providers import company
from orders import create_app
from orders.config import TestingConfig


@pytest.fixture
def app():
    app = create_app(TestingConfig)
    app_context = app.test_request_context()
    app_context.push()

    yield app

    app_context.pop()


@pytest.fixture
def db(app):
    from orders import db
    db.create_all()

    yield db

    db.session.remove()
    db.drop_all()


@pytest.fixture(scope="session")
def fake():
    f = Faker()
    f.add_provider(company)
    # f.seed(123)
    return f
