# pylint: disable=unused-variable,unused-argument,expression-not-assigned,singleton-comparison

import pytest
from expecter import expect

from .utils import load


def describe_root():

    def describe_index():

        @pytest.fixture
        def url():
            return "/api"

        def describe_GET():

            def it_returns_metadata(client, url):
                status, content = load(client.get(url))

                expect(status) == 200
                expect(content) == {
                    '_links': {
                        'self': "http://localhost/api",
                        'collections': "http://localhost/api/collections/",
                    }
                }

        def redirects_with_slash(client, url):
            status, content = load(client.get(url + "/"))

            expect(status) == 302


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
                    '_items': [
                        {
                            '_links': {
                                'self': "http://localhost/api/collections/abc123",
                                'items': "http://localhost/api/collections/abc123/items",
                                'votes': "http://localhost/api/collections/abc123/votes",
                                'scores': "http://localhost/api/collections/abc123/scores",
                            },
                            'key': "abc123",
                            'name': "Sample List",
                            'owner': "",
                            'code': "sample",
                            'private': False,
                            'locked': False,
                            'items': [
                                "bar",
                                "foo",
                                "qux",
                            ],
                            'vote_count': 1,
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
                expect(content['items']) == ["a", "b", "c"]

            def it_creates_an_empty_list_when_not_provided(client, url):
                data = {'name': "Foobar"}
                status, content = load(client.post(url, data=data))

                expect(status) == 201
                expect(content['name']) == "Foobar"
                expect(len(content['items'])) == 0

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
            return "/api/collections/abc123"

        def describe_GET():

            def it_returns_info_on_the_collection(client, url, collection):
                status, content = load(client.get(url))

                expect(status) == 200
                expect(content) == {
                    '_links': {
                        'self': "http://localhost/api/collections/abc123",
                        'items': "http://localhost/api/collections/abc123/items",
                        'votes': "http://localhost/api/collections/abc123/votes",
                        'scores': "http://localhost/api/collections/abc123/scores",
                    },
                    'key': "abc123",
                    'name': "Sample List",
                    'owner': "",
                    'code': "sample",
                    'private': False,
                    'locked': False,
                    'items': [
                        "bar",
                        "foo",
                        "qux",
                    ],
                    'vote_count': 1,
                }

            def when_missing(client):
                status, content = load(client.get("/api/collections/unknown"))

                expect(status) == 404

            def with_code(client, collection):
                url = "/api/collections/unknown?code=sample"
                status, content = load(client.get(url))

                expect(status) == 200
                expect(content['key']) == "abc123"

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

                status, content = load(client.delete(url))

                expect(status) == 204

                status, content = load(client.get(url))

                expect(status) == 404


def describe_items():

    def describe_index():

        @pytest.fixture
        def url():
            return "/api/collections/abc123/items"

        def describe_GET():

            def it_returns_the_list_of_items(client, url, collection):
                status, content = load(client.get(url))

                expect(status) == 200
                expect(content) == {
                    '_links': {
                        'self': "http://localhost/api/collections/abc123/items",
                        'collection': "http://localhost/api/collections/abc123",
                    },
                    '_objects': [
                        {
                            '_links': {
                                'self': "http://localhost/api/items/d4",
                            },
                            'key': "d4",
                            'name': "bar",
                            'description': None,
                            'image_url': None,
                            'ref_url': None,
                        },
                        {
                            '_links': {
                                'self': "http://localhost/api/items/f5",
                            },
                            'key': "f5",
                            'name': "foo",
                            'description': None,
                            'image_url': None,
                            'ref_url': None,
                        },
                        {
                            '_links': {
                                'self': "http://localhost/api/items/g6",
                            },
                            'key': "g6",
                            'name': "qux",
                            'description': None,
                            'image_url': None,
                            'ref_url': None,
                        },
                    ],
                }

            def when_unknown(client):
                url = "/api/collections/unknown/items"
                status, content = load(client.get(url))

                expect(status) == 404

        def describe_POST():

            def it_appends_to_the_list(client, url, collection):
                assert len(collection.items) == 3

                data = {'name': "new"}
                status, content = load(client.post(url, data=data))

                expect(status) == 200
                expect(len(content['_objects'])) == 4

            def when_missing(client, url):
                data = {'name': "Foobar"}
                status, content = load(client.post(url, data=data))

                expect(status) == 404

            def without_name(client, url, collection):
                status, content = load(client.post(url))

                expect(status) == 422
                expect(content['message']) == "Name is required."

        def describe_DELETE():

            def it_removes_an_item_by_name(client, url, collection):
                url += "/foo"
                status, content = load(client.delete(url))

                expect(status) == 200
                expect(content) == ["bar", "qux"]

            def unknown_items_are_ignored(client, url, collection):
                url += "/unknown"
                status, content = load(client.delete(url))

                expect(status) == 200
                expect(content) == ["bar", "foo", "qux"]

            def with_unknown_collection(client):
                url = "/api/collections/unknown/items/foo"
                status, content = load(client.delete(url))

                expect(status) == 404

    def describe_detail():

        @pytest.fixture
        def url():
            return "/api/items/_item"

        def describe_GET():

            def it_returns_info_on_the_item(client, url, item):
                status, content = load(client.get(url))

                expect(status) == 200
                expect(content) == {
                    '_links': {
                        'self': "http://localhost/api/items/_item",
                    },
                    'key': "_item",
                    'name': "Sample Item",
                    'description': "This is the sample item.",
                    'image_url': "http://www.gstatic.com/webp/gallery/1.jpg",
                    'ref_url': "http://example.com",
                }

            def when_unknown(client):
                status, content = load(client.get("/api/items/unknown"))

                expect(status) == 404


def describe_votes():

    @pytest.fixture
    def url():
        return "/api/collections/abc123/votes"

    def describe_GET():

        def it_returns_a_prioritized_list(client, url, collection):
            status, content = load(client.get(url))

            expect(status) == 200
            expect(content['_links']) == {
                'self': "http://localhost/api/collections/abc123/votes",
                'collection': "http://localhost/api/collections/abc123",
            },
            expect(content['name']) == "Sample List"
            expect(len(content['item_data'])) == 3

    def describe_POST():

        def it_records_a_new_vote(client, url, collection):
            data = {'winner': "foo", 'loser': "bar"}
            status, content = load(client.post(url, data=data))

            expect(status) == 200
            # TODO: check for vote

        def it_requires_winner_and_loser(client, url, collection):
            status, content = load(client.post(url))

            expect(status) == 422
            expect(content) == {
                'message': "Loser and winner are required.",
            }

        def with_unknown_collection(client):
            url = "/api/collections/unknown/votes"
            data = {'winner': "foo", 'loser': "bar"}
            status, content = load(client.post(url, data=data))

            expect(status) == 404

    def describe_DELETE():

        def it_clears_all_votes(client, url, collection):
            status, content = load(client.delete(url))

            expect(status) == 200
            expect(content['vote_count']) == 0

        def with_unknown_collection(client):
            url = "/api/collections/unknown/votes"
            status, content = load(client.delete(url))

            expect(status) == 404


def describe_scores():

    @pytest.fixture
    def url():
        return "/api/collections/abc123/scores"

    def describe_GET():

        def it_returns_scores(client, url, collection):
            status, content = load(client.get(url))

            expect(status) == 200
            expect(content) == {
                '_links': {
                    'self': "http://localhost/api/collections/abc123/scores",
                    'collection': "http://localhost/api/collections/abc123",
                },
                'name': "Sample List",
                'code': "sample",
                'private': False,
                'locked': False,
                'item_count': 3,
                'vote_count': 1,
                'scores': [
                    {
                        'name': "foo",
                        'points': 1.0,
                        'confidence': 0.5,
                    },
                    {
                        'name': "qux",
                        'points': 0.0,
                        'confidence': 0.0,
                    },
                    {
                        'name': "bar",
                        'points': -1.0,
                        'confidence': 0.5,
                    },
                ],
            }

        def with_inferred_votes(client, url, collection_inferred):
            status, content = load(client.get(url))

            expect(status) == 200
            expect(content['item_count']) == 3
            expect(content['vote_count']) == 2
            expect(content['scores']) == [
                {
                    'name': "foo",
                    'points': 1.9,
                    'confidence': 0.95,
                },
                {
                    'name': "bar",
                    'points': 0.0,
                    'confidence': 1.0,
                },
                {
                    'name': "qux",
                    'points': -1.9,
                    'confidence': 0.95,
                },
            ]

        def the_collection_must_exist(client, url):
            status, content = load(client.get(url))

            expect(status) == 404
