# pylint: disable=unused-variable,unused-argument

from expecter import expect

from .utils import get


def describe_index():

    def it_contains_link_to_sample_collection(client):
        html = get(client, "/")

        expect(html).contains('href="/test"')


def describe_collections():

    def describe_items():

        def with_known_key(client, collection):
            html = get(client, "/collections/abc123")

            expect(html).contains("Sample List")

        def with_unknown_key(client):
            html = get(client, "/collections/unknown")

            expect(html).contains("No Such Collection")
            expect(html).contains("Items: 0")

        def with_known_code(client, collection):
            html = get(client, "/sample")

            expect(html).contains("Sample List")

        def with_unknown_code(client, collection):
            html = get(client, "/unknown")

            expect(html).contains("No Such Collection")
            expect(html).contains("Items: 0")

    def describe_votes():

        def with_unknown_key(client):
            html = get(client, "/collections/unknown/vote")

            expect(html).contains("No Such Collection")

        def with_unknown_code(client):
            html = get(client, "/unknown/vote")

            expect(html).contains("No Such Collection")
