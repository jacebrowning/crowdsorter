# pylint: disable=unused-variable,unused-argument,redefined-outer-name

from expecter import expect

from .utils import get


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

    def describe_items():

        def with_known_code(client, collection):
            html = get(client, "/sample")

            expect(html).contains('<a href="/sample">Items</a>')
            expect(html).contains('<a href="/sample/vote">Vote</a>')
            expect(html).contains("Sample List")
            expect(html).contains("Items: 3")

        def with_unknown_code(client, collection):
            html = get(client, "/unknown")

            expect(html).contains("No Such Collection")
            expect(html).contains("Items: 0")

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
