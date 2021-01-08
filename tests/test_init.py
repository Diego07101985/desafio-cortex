from desafio.app import create_app
from desafio.settings import TestConfig


def test_config():
    assert create_app(TestConfig).testing
