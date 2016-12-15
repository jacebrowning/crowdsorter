# pylint: disable=unused-variable,unused-argument

from expecter import expect

from .utils import get


def describe_index():

    def it_contains_link_to_sample_collection(client):
        html = get(client, "/")

        expect(html).contains('href="/collections/test"')


def describe_collections():

    def describe_items():

        def with_unknown_code(client):
            html = get(client, "/collections/unknown")

            expect(html).contains("No Such Collection")

    def describe_votes():

        def with_unknown_code(client):
            html = get(client, "/collections/unknown/vote")

            expect(html).contains("No Such Collection")
