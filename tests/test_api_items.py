# pylint: disable=unused-variable,unused-argument,expression-not-assigned,singleton-comparison

import pytest
from expecter import expect

from .utils import load


def describe_items():

    def describe_index():

        @pytest.fixture
        def url():
            return "/api/collections/_c/items/"

        def describe_GET():

            def it_returns_the_list_of_items(client, url, collection):
                status, content = load(client.get(url))

                expect(status) == 200
                expect(content) == {
                    '_links': {
                        'self': "http://localhost/api/collections/_c/items/",
                        'collection': "http://localhost/api/collections/_c",
                    },
                    '_objects': [
                        {
                            '_links': {
                                'self': "http://localhost/api/items/_i1",
                            },
                            'key': "_i1",
                            'name': "bar",
                            'description': "",
                            'image_url': "",
                            'ref_url': "",
                            'enabled': True,
                        },
                        {
                            '_links': {
                                'self': "http://localhost/api/items/_i2",
                            },
                            'key': "_i2",
                            'name': "foo",
                            'description': "",
                            'image_url': "",
                            'ref_url': "",
                            'enabled': True,
                        },
                        {
                            '_links': {
                                'self': "http://localhost/api/items/_i3",
                            },
                            'key': "_i3",
                            'name': "qux",
                            'description': "",
                            'image_url': "",
                            'ref_url': "",
                            'enabled': True,
                        },
                    ],
                }

            def when_unknown(client):
                url = "/api/collections/unknown/items/"
                status, content = load(client.get(url))

                expect(status) == 404

        def describe_POST():

            def it_appends_to_the_list(client, url, collection):
                assert len(collection.items) == 3

                data = {'name': "new"}
                status, content = load(client.post(url, data=data))

                expect(status) == 200
                expect(len(content['_objects'])) == 4
                expect(content['_objects'][-1]['description']) == ""
                expect(content['_objects'][-1]['image_url']) == ""
                expect(content['_objects'][-1]['ref_url']) == ""

            def with_metadata(client, url, collection):
                data = {
                    'name': "Sample Item",
                    'description': "The item description.",
                    'image_url': "http://image.url",
                    'ref_url': "http://ref.url",
                }
                status, content = load(client.post(url, data=data))

                # Remove values that are non-deterministic
                del content['_objects'][-1]['_links']
                del content['_objects'][-1]['key']

                expect(status) == 200
                expect(content['_objects'][-1]) == {
                    'name': "Sample Item",
                    'description': "The item description.",
                    'image_url': "http://image.url",
                    'ref_url': "http://ref.url",
                    'enabled': True,
                }

            def when_missing(client, url):
                data = {'name': "Foobar"}
                status, content = load(client.post(url, data=data))

                expect(status) == 404

            def without_name(client, url, collection):
                status, content = load(client.post(url))

                expect(status) == 422
                expect(content['message']) == "Name is required."

            def with_duplicate_name(client, url, collection):
                data = {'name': "foo"}
                status, content = load(client.post(url, data=data))

                expect(status) == 409
                expect(content['message']) == "Item name is already taken."

        def describe_DELETE():

            def it_removes_an_item_by_name(client, url, collection):
                status, content = load(client.delete(url + "foo"))

                expect(status) == 200
                expect(content) == ["bar", "qux"]

            def unknown_items_are_ignored(client, url, collection):
                status, content = load(client.delete(url + "unknown"))

                expect(status) == 200
                expect(content) == ["bar", "foo", "qux"]

            def with_unknown_collection(client):
                url = "/api/collections/unknown/items/foo"
                status, content = load(client.delete(url))

                expect(status) == 404

    def describe_detail():

        @pytest.fixture
        def url():
            return "/api/items/_i"

        def describe_GET():

            def describe_nested():

                def it_redirects_to_the_unnested_item(client, collection):
                    item = collection.items[0]
                    url = "/api/collections/{}/items/{}".format(collection.key,
                                                                item.key)

                    status, content = load(client.get(url))

                    expect(status) == 302
                    expect(content).contains('href="/api/items/_i1"')

                def when_unknown_collection(client):
                    url = "/api/collections/_u/items/_u"

                    status, content = load(client.get(url))

                    expect(status) == 404

                def when_unknown_item(client, collection):
                    url = "/api/collections/{}/items/_u".format(collection.key)

                    status, content = load(client.get(url))

                    expect(status) == 404

            def it_returns_info_on_the_item(client, url, item):
                status, content = load(client.get(url))

                expect(status) == 200
                expect(content) == {
                    '_links': {
                        'self': "http://localhost/api/items/_i",
                    },
                    'key': "_i",
                    'name': "Sample Item",
                    'description': "This is the sample item.",
                    'image_url': "http://www.gstatic.com/webp/gallery/1.jpg",
                    'ref_url': "http://example.com",
                    'enabled': True,
                }

            def when_unknown(client):
                status, content = load(client.get("/api/items/unknown"))

                expect(status) == 404

        def describe_PUT():

            def it_can_update_the_name(client, url, item):
                data = {'name': "Updated Name  "}
                status, content = load(client.put(url, data=data))

                expect(status) == 200
                expect(content['name']) == "Updated Name"

            def it_ignores_empty_names(client, url, item):
                data = {'name': "  "}
                status, content = load(client.put(url, data=data))

                expect(status) == 200
                expect(content['name']) == "Sample Item"

            def it_can_update_the_description(client, url, item):
                data = {'description': "The description.  "}
                status, content = load(client.put(url, data=data))

                expect(status) == 200
                expect(content['description']) == "The description."

            def it_can_clear_the_description(client, url, item):
                data = {'description': "  "}
                status, content = load(client.put(url, data=data))

                expect(status) == 200
                expect(content['description']) == ""

            def it_can_update_the_image_url(client, url, item):
                data = {'image_url': "http://example.com/image.jpg"}
                status, content = load(client.put(url, data=data))

                expect(status) == 200
                expect(content['image_url']) == "http://example.com/image.jpg"

            def it_rejects_invalid_image_urls(client, url, item):
                data = {'image_url': "http://foo"}
                status, content = load(client.put(url, data=data))

                expect(status) == 422
                expect(content['message']) == "Invalid URL: http://foo"

            def it_can_update_the_ref_url(client, url, item):
                data = {'ref_url': "http://example.com/ref"}
                status, content = load(client.put(url, data=data))

                expect(status) == 200
                expect(content['ref_url']) == "http://example.com/ref"

            def it_rejects_invalid_ref_urls(client, url, item):
                data = {'ref_url': "http://foo"}
                status, content = load(client.put(url, data=data))

                expect(status) == 422
                expect(content['message']) == "Invalid URL: http://foo"

            def it_can_disable_an_item(client, url, item):
                data = {'enabled': False}
                status, content = load(client.put(url, data=data))

                expect(status) == 200
                expect(content['enabled']) == False

        def describe_DELETE():

            def it_removes_the_item_from_collections(client, url, collection):
                item = collection.items[0]
                get_url = ("/api/collections/{collection.key}/items/{item.key}"
                           "".format(collection=collection, item=item))
                delete_url = "/api/items/{item.key}".format(item=item)

                status, content = load(client.get(get_url))
                expect(status) == 302

                status, content = load(client.delete(delete_url))
                expect(status) == 204

                status, content = load(client.get(get_url))
                expect(status) == 404

            def it_can_be_called_multiple_times(client, url, collection):
                for _ in range(2):
                    status, content = load(client.delete(url))

                    expect(status) == 204
