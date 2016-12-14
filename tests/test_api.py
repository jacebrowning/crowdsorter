# pylint: disable=unused-variable,unused-argument,expression-not-assigned

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
                expect(content['items']) == ["a", "c", "b"]

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

    def describe_detail():

        @pytest.fixture
        def url():
            return "/api/collections/abc123"

        def describe_GET():

            def it_returns_info_on_the_collection(client, url, collection):
                status, content = load(client.get(url))

                expect(status) == 200
                expect(content) == {
                    'uri': "http://localhost/api/collections/abc123",
                    'key': "abc123",
                    'name': "Sample List",
                    'items': [],
                }


def describe_items():

    @pytest.fixture
    def url():
        return "/api/collections/abc123/items"

    def describe_GET():

        def it_returns_a_list(client, url, collection):
            status, content = load(client.get(url))

            expect(status) == 200
            expect(content) == []

    def describe_POST():

        def it_appends_to_the_list(client, url, collection):
            data = {'name': "Foobar"}
            status, content = load(client.post(url, data=data))

            expect(status) == 200
            expect(content) == [
                "Foobar",
            ]

        def the_collection_must_exist(client, url):
            data = {'name': "Foobar"}
            status, content = load(client.post(url, data=data))

            expect(status) == 404

        def it_requires_a_name(client, url, collection):
            status, content = load(client.post(url))

            expect(status) == 422
            expect(content['message']) == "Name is required."
