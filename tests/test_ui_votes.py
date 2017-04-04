# pylint: disable=unused-variable,unused-argument,redefined-outer-name,expression-not-assigned

from expecter import expect

from .utils import get, post


def describe_votes():

    def describe_results():

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

        def describe_add_item():

            def with_name(client, collection):
                data = dict(name="New Item")
                html = post(client, "/sample", data)

                expect(html).contains("Added item: New Item")

            def on_locked_collection(client, collection_locked):
                data = dict(name="New Item")
                html = post(client, "/sample", data)

                expect(html).contains("Unable to add items.")

    def describe_cast():

        def with_known_code(client, collection):
            html = get(client, "/sample/vote")

            expect(html).contains('<a href="/sample">Results</a>')
            expect(html).contains('<a href="/sample/vote">Vote</a>')
            expect(html).contains("Sample List")
            expect(html).contains("Next Pair")

        def with_unknown_code(client):
            html = get(client, "/unknown/vote")

            expect(html).contains("Not Found")