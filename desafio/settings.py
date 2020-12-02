# -*- coding: utf-8 -*-
"""Application configuration."""
import os


class Config(object):
    """Base configuration."""

    SECRET_KEY = os.environ.get(
        'CONDUIT_SECRET', 'secret-key')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = True
    CACHE_TYPE = "redis"
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_REDIS_HOST = "redis"
    CACHE_REDIS_PORT = 6379
    SECRET_KEY = ""
    FLASK_PIKA_PARAMS = {
        'host': 'rabbitmq',  # amqp.server.com
        'username': 'rabbitmq',  # convenience param for username
        'password': 'rabbitmq',  # convenience param for password
        'port': 5672,  # amqp server port
    }
    FLASK_PIKA_POOL_PARAMS = {
        'pool_size': 1024,
        'pool_recycle': 10
    }


class TestConfig(Config):
    """Test configuration."""
    TESTING = True
    DEBUG = True
    SECRET_KEY = "test"
    CACHE_TYPE = "redis"
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379

    FLASK_PIKA_PARAMS = {
        'host': 'localhost',  # amqp.server.com
        'username': 'rabbitmq',  # convenience param for username
        'password': 'rabbitmq',  # convenience param for password
        'port': 5672,  # amqp server port
    }
    FLASK_PIKA_POOL_PARAMS = {
        'pool_size': 1024,
        'pool_recycle': 10
    }
