# pylint: disable=unused-variable,unused-argument,expression-not-assigned

from expecter import expect

from .utils import load


def describe_root():

    def describe_index():

        def describe_GET():

            def it_returns_metadata(client):
                status, content = load(client.get("/api"))

                expect(status) == 200
                expect(content) == {
                    'collections': "http://localhost/api/collections/"
                }


def describe_collections():

    def describe_index():

        def describe_GET():

            def it_returns_a_list_of_rooms(client, collection):
                status, content = load(client.get("/api/collections/"))

                expect(status) == 200
                expect(content) == []
