# pylint: disable=unused-variable,unused-argument,redefined-outer-name

from expecter import expect

from .utils import get, post


def describe_index():

    def it_contains_link_to_sample_collection(client):
        html = get(client, "/")

        expect(html).contains('href="/collections/"')


def describe_collections():

    def describe_index():

        def with_collections(client, collection):
            html = get(client, "/collections/")

            expect(html).contains("Popular Collections")
            expect(html).contains('<a href="/test" class="list-group-item">')
            expect(html).contains('<a href="/sample" class="list-group-item">')

        def describe_new():

            def with_name(client):
                data = {'name': "My List"}
                html = post(client, "/collections/", data)

                expect(html).contains("Created collection: My List")
                expect(html).contains("My List")

            def without_name(client):
                data = {}
                html = post(client, "/collections/", data)

                expect(html).contains("A name is required.")

    def describe_items():

        def with_known_code(client, collection):
            html = get(client, "/sample")

            expect(html).contains('<a href="/sample">Items</a>')
            expect(html).contains('<a href="/sample/vote">Vote</a>')
            expect(html).contains("Sample List")
            expect(html).contains("Items: 3")
            expect(html).contains('value="Add Item">')

        def with_unknown_code(client, collection):
            html = get(client, "/unknown")

            expect(html).contains("No Such Collection")
            expect(html).contains("Items: 0")
            expect(html).does_not_contain('value="Add Item">')

        def describe_add():

            def with_name(client, collection):
                data = dict(name="New Item")
                html = post(client, "/sample", data)

                expect(html).contains("Added item: New Item")

            def on_locked_collection(client, collection_locked):
                data = dict(name="New Item")
                html = post(client, "/sample", data)

                expect(html).contains("Unable to add items.")

    def describe_votes():

        def with_known_code(client, collection):
            html = get(client, "/sample/vote")

            expect(html).contains('<a href="/sample">Items</a>')
            expect(html).contains('<a href="/sample/vote">Vote</a>')
            expect(html).contains("Sample List")
            expect(html).contains("Get New Comparison Pair")

        def with_unknown_code(client):
            html = get(client, "/unknown/vote")

            expect(html).contains("No Such Collection")


def describe_admin():

    def with_known_key(client, collection):
        html = get(client, "/collections/abc123")

        expect(html).contains('<a href="/collections/abc123">Admin</a>')
        expect(html).contains("Sample List")

    def with_unknown_key(client):
        html = get(client, "/collections/unknown")

        expect(html).contains("No Such Collection")

    def describe_save():

        def with_locked_set(client, collection):
            data = dict(save=True, unlocked=[])
            html = post(client, "/collections/abc123", data)

            expect(html).contains("Options updated.")
            expect(html).contains('name="unlocked" >')

        def with_locked_clear(client, collection):
            data = dict(save=True, unlocked=['on'])
            html = post(client, "/collections/abc123", data)

            expect(html).contains("Options updated.")
            expect(html).contains('name="unlocked" checked=true>')

        def with_private_set(client, collection):
            data = dict(save=True, public=[])
            html = post(client, "/collections/abc123", data)

            expect(html).contains("Options updated.")
            expect(html).contains('name="public" >')

        def with_private_clear(client, collection):
            data = dict(save=True, public=['on'])
            html = post(client, "/collections/abc123", data)

            expect(html).contains("Options updated.")
            expect(html).contains('name="public" checked=true>')

    def describe_add():

        def with_name(client, collection):
            data = dict(add="New Item")
            html = post(client, "/collections/abc123", data)

            expect(html).contains("Added item: New Item")
            expect(html).contains(' value="New Item" name="remove">')

    def describe_remove():

        def with_name(client, collection):
            data = dict(remove="foo")
            html = post(client, "/collections/abc123", data)

            expect(html).contains("Removed item: foo")
            expect(html).does_not_contain(' value="foo" name="remove">')
