import os


class Config:
    """Base configuration."""

    ENV = None

    PATH = os.path.abspath(os.path.dirname(__file__))
    ROOT = os.path.dirname(PATH)
    DEBUG = False
    THREADED = False

    SAMPLE_COLLECTION_KEY = os.getenv('SAMPLE_COLLECTION_KEY')

    GOOGLE_ANALYTICS_ID = os.getenv('GOOGLE_ANALYTICS_ID')


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'

    SECRET_KEY = os.getenv('SECRET_KEY')
    MONGODB_HOST = os.getenv('MONGODB_URI')


class TestConfig(Config):
    """Test configuration."""

    ENV = 'test'

    DEBUG = True
    TESTING = True

    SECRET_KEY = 'test'
    MONGODB_DB = 'crowdsorter_test'

    SAMPLE_COLLECTION_KEY = 'test'


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'

    DEBUG = True

    SECRET_KEY = 'dev'
    MONGODB_DB = 'crowdsorter_dev'

    SAMPLE_COLLECTION_KEY = '_sample'


def get_config(name):
    assert name, "no configuration specified"

    for config in Config.__subclasses__():
        if config.ENV == name:
            return config

    assert False, "no matching configuration"
