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
    collection = Collection(name="Sample List", key='_c', code='sample')
    collection.items = [
        Item(name="bar", key='_i1').save(),
        Item(name="foo", key='_i2').save(),
        Item(name="qux", key='_i3').save(),
    ]
    collection.vote("foo", "bar")
    collection.save()
    return collection


@pytest.fixture
def collection2():
    collection = Collection(name="Sample List 2", key='_c2')
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
    item = Item(name="Sample Item", key='_i')
    item.description = "This is the sample item."
    item.image_url = "http://www.gstatic.com/webp/gallery/1.jpg"
    item.ref_url = "http://example.com"
    item.save()
    return item
