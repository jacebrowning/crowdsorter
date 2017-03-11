# pylint: disable=unused-variable,unused-argument,expression-not-assigned,singleton-comparison

import pytest
from expecter import expect

from .utils import load


def describe_votes():

    @pytest.fixture
    def url():
        return "/api/collections/_c/votes/"

    def describe_GET():

        def it_returns_a_prioritized_list(client, url, collection):
            status, content = load(client.get(url))

            expect(status) == 200
            expect(content['_links']) == {
                'self': "http://localhost/api/collections/_c/votes/",
                'collection': "http://localhost/api/collections/_c",
            },
            expect(content['name']) == "Sample List"
            expect(len(content['item_data'])) == 3

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
                'message': "Loser and winner are required.",
            }

        def with_unknown_collection(client):
            url = "/api/collections/unknown/votes/"
            data = {'winner': "foo", 'loser': "bar"}
            status, content = load(client.post(url, data=data))

            expect(status) == 404

    def describe_DELETE():

        def it_clears_all_votes(client, url, collection):
            status, content = load(client.delete(url))

            expect(status) == 200
            expect(content['vote_count']) == 0

        def with_unknown_collection(client):
            url = "/api/collections/unknown/votes/"
            status, content = load(client.delete(url))

            expect(status) == 404
