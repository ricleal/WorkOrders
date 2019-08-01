import pytest
from faker import Faker
from orders import create_app
from orders.config import TestingConfig


@pytest.fixture
def app():
    app = create_app(TestingConfig)
    app.test_request_context().push()
    return app


@pytest.fixture
def fake():
    f = Faker()
    #f.seed(123)
    return f
