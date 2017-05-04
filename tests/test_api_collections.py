# pylint: disable=unused-variable,unused-argument,expression-not-assigned,singleton-comparison

import pytest
from expecter import expect

from .utils import load


def describe_collections():

    def describe_index():

        @pytest.fixture
        def url():
            return "/api/collections/"

        def describe_GET():

            def it_requires_auth(client, url, collection):
                status, content = load(client.get(url))

                expect(status) == 403

            def it_returns_a_list_of_collections(client, url, collection):
                status, content = load(client.get(url + "?token=test"))

                expect(status) == 200
                expect(content) == {
                    '_links': {
                        'root': "http://localhost/api",
                        'self': "http://localhost/api/collections/",
                    },
                    '_objects': [
                        {
                            '_links': {
                                'self': "http://localhost/api/collections/_c",
                                'items': "http://localhost/api/collections/_c/items/",
                                'votes': "http://localhost/api/collections/_c/votes/",
                                'scores': "http://localhost/api/collections/_c/scores/",
                            },
                            'key': "_c",
                            'name': "Sample List",
                            'owner': "",
                            'code': "sample",
                            'private': False,
                            'locked': False,
                            'vote_count': 1,
                            '_embedded': {},
                        },
                    ],

                }

        def describe_POST():

            def it_creates_a_new_collection(client, url):
                data = {'name': "Foobar", 'items': ["a", "c", "b"]}
                status, content = load(client.post(url, data=data))

                expect(status) == 201
                expect(content['name']) == "Foobar"
                expect(content['code']) != None
                expect(len(content['_embedded']['items'])) == 3

            def it_creates_an_empty_list_when_not_provided(client, url):
                data = {'name': "Foobar"}
                status, content = load(client.post(url, data=data))

                expect(status) == 201
                expect(content['name']) == "Foobar"
                expect(len(content['_embedded']['items'])) == 0

            def it_requires_a_name(client, url):
                status, content = load(client.post(url))

                expect(status) == 422
                expect(content['message']) == "Name is required."

            def a_code_can_be_provided(client, url):
                data = {'name': "Foobar", 'code': "my-code"}
                status, content = load(client.post(url, data=data))

                expect(status) == 201
                expect(content['name']) == "Foobar"
                expect(content['code']) == "my-code"

    def describe_detail():

        @pytest.fixture
        def url():
            return "/api/collections/_c"

        def describe_GET():

            def it_returns_info_on_the_collection(client, url, collection):
                status, content = load(client.get(url))

                expect(status) == 200
                expect(content) == {
                    '_links': {
                        'self': "http://localhost/api/collections/_c",
                        'items': "http://localhost/api/collections/_c/items/",
                        'votes': "http://localhost/api/collections/_c/votes/",
                        'scores': "http://localhost/api/collections/_c/scores/",
                    },
                    'key': "_c",
                    'name': "Sample List",
                    'owner': "",
                    'code': "sample",
                    'private': False,
                    'locked': False,
                    'vote_count': 1,
                    '_embedded': {
                        'items': [
                            {
                                '_links': {
                                    'self': "http://localhost/api/items/_i1",
                                },
                                # pylint: disable=duplicate-code
                                'key': "_i1",
                                'name': "bar",
                                'description': "",
                                'image_url': "",
                                'ref_url': "",
                                'enabled': True,
                            },
                            # pylint: disable=duplicate-code
                            {
                                '_links': {
                                    'self': "http://localhost/api/items/_i2",
                                },
                                # pylint: disable=duplicate-code
                                'key': "_i2",
                                'name': "foo",
                                'description': "",
                                'image_url': "",
                                'ref_url': "",
                                'enabled': True,
                            },
                            # pylint: disable=duplicate-code
                            {
                                '_links': {
                                    'self': "http://localhost/api/items/_i3",
                                },
                                # pylint: disable=duplicate-code
                                'key': "_i3",
                                'name': "qux",
                                'description': "",
                                'image_url': "",
                                'ref_url': "",
                                'enabled': True,
                            },
                        ],
                    },
                }

            def when_missing(client):
                status, content = load(client.get("/api/collections/unknown"))

                expect(status) == 404

            def with_code(client, collection):
                url = "/api/collections/unknown?code=sample"
                status, content = load(client.get(url))

                expect(status) == 200
                expect(content['key']) == "_c"

        def describe_PUT():

            def it_can_update_the_owner_email(client, url, collection):
                data = {'owner': "test@example.com"}
                status, content = load(client.put(url, data=data))

                expect(status) == 200
                expect(content['owner']) == "test@example.com"

            def valid_email_addresses_are_required(client, url, collection):
                data = {'owner': "@foo.com"}
                status, content = load(client.put(url, data=data))

                expect(status) == 422
                expect(content['message']) == "Invalid email address: @foo.com"

            def it_can_update_the_name(client, url, collection):
                data = {'name': "New Name  "}
                status, content = load(client.put(url, data=data))

                expect(status) == 200
                expect(content['name']) == "New Name"

            def it_ignores_empty_names(client, url, collection):
                data = {'name': "  "}
                status, content = load(client.put(url, data=data))

                expect(status) == 200
                expect(content['name']) == "Sample List"

            def it_can_update_the_code(client, url, collection):
                data = {'code': "def 456  "}
                status, content = load(client.put(url, data=data))

                expect(status) == 200
                expect(content['code']) == "def-456"

            def it_ignores_empty_codes(client, url, collection):
                data = {'code': "  "}
                status, content = load(client.put(url, data=data))

                expect(status) == 200
                expect(content['code']) == "sample"

            def it_can_set_the_private_flag(client, url, collection):
                data = {'private': True}
                status, content = load(client.put(url, data=data))

                expect(status) == 200
                expect(content['private']) == True

            def it_can_clear_the_private_flag(client, url, collection):
                data = {'private': False}
                status, content = load(client.put(url, data=data))

                expect(status) == 200
                expect(content['private']) == False

            def it_can_set_the_locked_flag(client, url, collection):
                data = {'locked': True}
                status, content = load(client.put(url, data=data))

                expect(status) == 200
                expect(content['locked']) == True

            def it_can_clear_the_locked_flag(client, url, collection):
                data = {'locked': False}
                status, content = load(client.put(url, data=data))

                expect(status) == 200
                expect(content['locked']) == False

        def describe_DELETE():

            def it_deletes_the_collection(client, url, collection):
                status, content = load(client.delete(url))
                expect(status) == 204

                status, content = load(client.get(url))
                expect(status) == 404

            def it_can_be_called_multiple_times(client, url, collection):
                for _ in range(2):
                    status, content = load(client.delete(url))

                    expect(status) == 204
