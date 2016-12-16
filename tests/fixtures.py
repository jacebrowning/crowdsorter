# pylint: disable=redefined-outer-name

import pytest

from crowdsorter.app import create_app
from crowdsorter.settings import get_config
from crowdsorter.models import Collection


@pytest.fixture
def app():
    return create_app(get_config('test'))


@pytest.fixture
def client(app):
    Collection.objects.delete()
    return app.test_client()


@pytest.fixture
def collection():
    collection = Collection(name="Sample List", key='abc123', code='sample')
    collection.items = ["bar", "foo"]
    collection.vote("foo", "bar")
    collection.save()
    return collection
