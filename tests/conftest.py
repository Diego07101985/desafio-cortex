import pytest
from desafio.app import create_app
from desafio.settings import TestConfig


@pytest.fixture(scope="session")
def app():
    app = create_app(TestConfig)
    yield app


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def runner(app):
    return app.test_cli_runner()
