# pylint: disable=unused-variable,unused-argument,expression-not-assigned,singleton-comparison

import pytest
from expecter import expect

from .utils import load


def describe_scores():

    @pytest.fixture
    def url():
        return "/api/collections/_c/scores/"

    def describe_GET():

        def it_returns_scores(client, url, collection):
            status, content = load(client.get(url))

            expect(status) == 200
            expect(content) == {
                '_links': {
                    'self': "http://localhost/api/collections/_c/scores/",
                    'collection': "http://localhost/api/collections/_c",
                },
                'name': "Sample List",
                'code': "sample",
                'private': False,
                'locked': False,
                'vote_count': 1,
                'item_data': [
                    {
                        'name': "foo",
                        'key': "_i2",
                        'points': 1.0,
                        'confidence': 0.5,
                    },
                    {
                        'name': "qux",
                        'key': "_i3",
                        'points': 0.0,
                        'confidence': 0.0,
                    },
                    {
                        'name': "bar",
                        'key': "_i1",
                        'points': -1.0,
                        'confidence': 0.5,
                    },
                ],
            }

        def with_inferred_votes(client, url, collection_inferred):
            status, content = load(client.get(url))

            expect(status) == 200
            expect(content['vote_count']) == 2
            expect(content['item_data']) == [
                {
                    'name': "foo",
                    'key': "_i2",
                    'points': 1.9,
                    'confidence': 0.95,
                },
                {
                    'name': "bar",
                    'key': "_i1",
                    'points': 0.0,
                    'confidence': 1.0,
                },
                {
                    'name': "qux",
                    'key': "_i3",
                    'points': -1.9,
                    'confidence': 0.95,
                },
            ]

        def locked_collections_hide_keys(client, url, collection):
            collection.locked = True
            collection.save()

            status, content = load(client.get(url))

            expect(status) == 200
            expect(content['item_data']) == [
                {
                    'name': "foo",
                    'points': 1.0,
                    'confidence': 0.5,
                },
                {
                    'name': "qux",
                    'points': 0.0,
                    'confidence': 0.0,
                },
                {
                    'name': "bar",
                    'points': -1.0,
                    'confidence': 0.5,
                },
            ]

        def the_collection_must_exist(client, url):
            status, content = load(client.get(url))

            expect(status) == 404
