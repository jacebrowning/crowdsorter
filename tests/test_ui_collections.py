# pylint: disable=unused-variable,unused-argument,redefined-outer-name,expression-not-assigned

from expecter import expect

from .utils import get, post


def describe_collections():

    def describe_index():

        def with_collections(client, collection):
            html = get(client, "/collections/")

            expect(html).contains("Popular Collections")
            expect(html).contains('<a href="/sample" class="list-group-item">')
            expect(html).contains("1 Votes")

        def describe_new():

            def with_name(client):
                data = {'name': "My List"}
                html = post(client, "/collections/", data)

                expect(html).contains("My List")
                expect(html).contains("This is the admin page")

            def without_name(client):
                data = {}
                html = post(client, "/collections/", data)

                expect(html).contains("A name is required.")

    def describe_items():

        def with_known_code(client, collection):
            html = get(client, "/sample")

            expect(html).contains('<a href="/sample">Results</a>')
            expect(html).contains('<a href="/sample/vote">Vote</a>')
            expect(html).contains("Sample List")
            expect(html).contains("Items: 3")
            expect(html).contains('glyphicon-plus-sign')
            expect(html).contains("Share on Facebook")

        def with_unknown_code(client, collection):
            html = get(client, "/unknown")

            expect(html).contains("Not Found")

        def on_private_collection(client, collection_private):
            html = get(client, "/sample")

            expect(html).does_not_contain("Share on Facebook")

        def on_collection_with_fewer_than_2_items(client, collection):
            while len(collection.items) >= 2:
                collection.items.pop()
            collection.save()

            html = get(client, "/sample")

            expect(html).contains(' disabled" href="/sample/vote"')

        def describe_add():

            def with_name(client, collection):
                data = dict(name="New Item")
                html = post(client, "/sample", data)

                expect(html).contains('<h2 class="title">New Item</h2>')

            def on_locked_collection(client, collection_locked):
                data = dict(name="New Item")
                html = post(client, "/sample", data)

                expect(html).contains("This window will close automatically...")

    def describe_votes():

        def with_known_code(client, collection):
            html = get(client, "/sample/vote")

            expect(html).contains('<a href="/sample">Results</a>')
            expect(html).contains('<a href="/sample/vote">Vote</a>')
            expect(html).contains("Sample List")
            expect(html).contains("Next Pair")

        def with_unknown_code(client):
            html = get(client, "/unknown/vote")

            expect(html).contains("Not Found")
