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
                    'collections': "http://localhost/api/collections/"
                }


def describe_collections():

    def describe_index():

        @pytest.fixture
        def url():
            return "/api/collections/"

        def describe_GET():

            def it_returns_a_list_of_collections(client, url, collection):
                status, content = load(client.get(url))

                expect(status) == 200
                expect(content) == [
                    "http://localhost/api/collections/abc123"
                ]

        def describe_POST():

            def it_creates_a_new_collection(client, url):
                data = {'name': "Foobar", 'items': ["a", "c", "b"]}
                status, content = load(client.post(url, data=data))

                expect(status) == 201
                expect(content['name']) == "Foobar"
                expect(content['code']) == None
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
                    'code': "sample",
                    'items': [
                        "bar",
                        "foo",
                        "qux",
                    ],
                }

            def when_missing(client):
                status, content = load(client.get("/api/collections/unknown"))

                expect(status) == 404

            def with_code(client, collection):
                url = "/api/collections/unknown?code=sample"
                status, content = load(client.get(url))

                expect(status) == 200
                expect(content['key']) == "abc123"


def describe_items():

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
                'items': [
                    "bar",
                    "foo",
                    "qux",
                ],
            }

        def when_missing(client):
            status, content = load(client.get("/api/collections/unknown/items"))

            expect(status) == 404

    def describe_POST():

        def it_appends_to_the_list(client, url, collection):
            data = {'name': "new"}
            status, content = load(client.post(url, data=data))

            expect(status) == 200
            expect(content) == {
                '_links': {
                    'self': "http://localhost/api/collections/abc123/items",
                    'collection': "http://localhost/api/collections/abc123",
                },
                'items': [
                    "bar",
                    "foo",
                    "new",
                    "qux",
                ],
            }

        def when_missing(client, url):
            data = {'name': "Foobar"}
            status, content = load(client.post(url, data=data))

            expect(status) == 404

        def without_name(client, url, collection):
            status, content = load(client.post(url))

            expect(status) == 422
            expect(content['message']) == "Name is required."


def describe_votes():

    @pytest.fixture
    def url():
        return "/api/collections/abc123/votes"

    def describe_GET():

        def it_returns_a_prioritized_list(client, url, collection):
            status, content = load(client.get(url))

            expect(status) == 200
            expect(content['name']) == "Sample List"
            expect(len(content['items'])) == 3

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
                'message': "Winner and loser are required.",
            }


def describe_scores():

    @pytest.fixture
    def url():
        return "/api/collections/abc123/scores"

    def describe_GET():

        def it_returns_scores(client, url, collection):
            status, content = load(client.get(url))

            expect(status) == 200
            expect(content) == {
                'name': "Sample List",
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
            expect(content) == {
                'name': "Sample List",
                'item_count': 3,
                'vote_count': 2,
                'scores': [
                    {
                        'name': "foo",
                        'points': 1.9,
                        'confidence': 0.75,
                    },
                    {
                        'name': "bar",
                        'points': 0.0,
                        'confidence': 1.0,
                    },
                    {
                        'name': "qux",
                        'points': -1.9,
                        'confidence': 0.75,
                    },
                ],
            }

        def the_collection_must_exist(client, url):
            status, content = load(client.get(url))

            expect(status) == 404
