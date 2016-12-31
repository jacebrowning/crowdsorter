import os


class Config:
    """Base configuration."""

    ENV = None

    PATH = os.path.abspath(os.path.dirname(__file__))
    ROOT = os.path.dirname(PATH)
    DEBUG = False
    THREADED = False
    SECRET_KEY = os.getenv('SECRET_KEY')

    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    SENDGRID_DEFAULT_FROM = os.getenv('SENDGRID_DEFAULT_FROM')

    AUTH_TOKEN = os.getenv('AUTH_TOKEN')
    SAMPLE_COLLECTION_CODE = os.getenv('SAMPLE_COLLECTION_CODE')
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

    SAMPLE_COLLECTION_CODE = ENV
    AUTH_TOKEN = ENV


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'

    DEBUG = True
    SECRET_KEY = ENV

    MONGODB_DB = 'crowdsorter_dev'

    SAMPLE_COLLECTION_CODE = 'sample'
    AUTH_TOKEN = ENV


def get_config(name):
    assert name, "no configuration specified"

    for config in Config.__subclasses__():
        if config.ENV == name:
            return config

    assert False, "no matching configuration"
