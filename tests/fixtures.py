# pylint: disable=redefined-outer-name

import pytest

from crowdsorter.settings import get_config
from crowdsorter.factory import create_app
from crowdsorter.models import Collection, Item


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
    collection.items2 = [
        Item(name="bar", key='d4').save(),
        Item(name="foo", key='f5').save(),
        Item(name="qux", key='g6').save(),
    ]
    collection.vote("foo", "bar")
    collection.save()
    return collection


@pytest.fixture
def collection2():
    collection = Collection(name="Sample List 2", key='def456')
    collection.save()
    return collection


@pytest.fixture
def collection_inferred(collection):
    collection.vote("bar", "qux")
    collection.save()
    return collection


@pytest.fixture
def collection_private(collection):
    collection.private = True
    collection.save()
    return collection


@pytest.fixture
def collection_locked(collection):
    collection.locked = True
    collection.save()
    return collection


@pytest.fixture
def item():
    item = Item(name="Sample Item", key='_item')
    item.save()
    return item
