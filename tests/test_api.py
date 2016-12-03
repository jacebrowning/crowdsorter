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

            def it_returns_a_list_of_collections(client, collection):
                status, content = load(client.get("/api/collections/"))

                expect(status) == 200
                expect(content) == [
                    "http://localhost/api/collections/abc123"
                ]

        def describe_POST():

            def it_creates_a_new_collection(client):
                data = {'name': "Foobar", 'items': ["a", "b"]}
                status, content = load(client.post("/api/collections/",
                                                   data=data))

                expect(status) == 201
                expect(content['name']) == "Foobar"
                expect(len(content['items'])) == 2

            def it_creates_an_empty_list_of_items_when_not_provided(client):
                data = {'name': "Foobar"}
                status, content = load(client.post("/api/collections/",
                                                   data=data))

                expect(status) == 201
                expect(content['name']) == "Foobar"
                expect(len(content['items'])) == 0

            def it_requires_a_name(client):
                status, content = load(client.post("/api/collections/"))

                expect(status) == 422
                expect(content['message']) == "Name is required."

    def describe_detail():

        def describe_GET():

            def it_returns_info_on_the_collection(client, collection):
                status, content = load(client.get("/api/collections/abc123"))

                expect(status) == 200
                expect(content) == {
                    'uri': "http://localhost/api/collections/abc123",
                    'name': "Sample List",
                    'items': [],
                }
