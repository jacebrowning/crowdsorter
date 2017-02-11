import os
from datetime import timedelta


class Config:
    """Base configuration."""

    ENV = None

    PATH = os.path.abspath(os.path.dirname(__file__))
    ROOT = os.path.dirname(PATH)
    DEBUG = False
    THREADED = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    SENDGRID_DEFAULT_FROM = os.getenv('SENDGRID_DEFAULT_FROM')

    AUTH_TOKEN = os.getenv('AUTH_TOKEN')
    GOOGLE_ANALYTICS_ID = os.getenv('GOOGLE_ANALYTICS_ID')


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'

    MONGODB_HOST = os.getenv('MONGODB_URI')


class TestConfig(Config):
    """Test configuration."""

    ENV = 'test'

    DEBUG = True
    TESTING = True
    SECRET_KEY = ENV

    MONGODB_DB = 'crowdsorter_test'
    SENDGRID_DEFAULT_FROM = 'test@example.com'

    AUTH_TOKEN = ENV


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'

    DEBUG = True
    SECRET_KEY = ENV

    MONGODB_DB = 'crowdsorter_dev'
    SENDGRID_DEFAULT_FROM = 'dev@example.com'

    AUTH_TOKEN = ENV


def get_config(name):
    assert name, "no configuration specified"

    for config in Config.__subclasses__():
        if config.ENV == name:
            return config

    assert False, "no matching configuration"
