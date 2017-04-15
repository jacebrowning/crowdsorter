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
                    'data': "http://localhost/api/collections/_c/scores/data/",
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
                        'image_url': None,
                        'ref_url': None,
                        'points': 1.0,
                        'confidence': 0.5,
                    },
                    {
                        'name': "qux",
                        'key': "_i3",
                        'image_url': None,
                        'ref_url': None,
                        'points': 0.0,
                        'confidence': 0.0,
                    },
                    {
                        'name': "bar",
                        'key': "_i1",
                        'image_url': None,
                        'ref_url': None,
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
                    'image_url': None,
                    'ref_url': None,
                    'points': 2.0,
                    'confidence': 2 / 3,
                },
                {
                    'name': "bar",
                    'key': "_i1",
                    'image_url': None,
                    'ref_url': None,
                    'points': 0.0,
                    'confidence': 1.0,
                },
                {
                    'name': "qux",
                    'key': "_i3",
                    'image_url': None,
                    'ref_url': None,
                    'points': -2.0,
                    'confidence': 2 / 3,
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
                    'image_url': None,
                    'ref_url': None,
                    'points': 1.0,
                    'confidence': 0.5,
                },
                {
                    'name': "qux",
                    'image_url': None,
                    'ref_url': None,
                    'points': 0.0,
                    'confidence': 0.0,
                },
                {
                    'name': "bar",
                    'image_url': None,
                    'ref_url': None,
                    'points': -1.0,
                    'confidence': 0.5,
                },
            ]

        def the_collection_must_exist(client, url):
            status, content = load(client.get(url))

            expect(status) == 404

    def describe_data():

        @pytest.fixture
        def url():
            return "/api/collections/_c/scores/data/"

        def describe_GET():

            def it_returns_data(client, url, collection):
                status, content = load(client.get(url))

                expect(status) == 200
                expect(content) == {
                    '_links': {
                        'self': "http://localhost/api/collections/_c/scores/data/",
                        'scores': "http://localhost/api/collections/_c/scores/",
                    },
                    'name': "Sample List",
                    'data': [
                        ['', 'bar', 'foo', 'qux'],
                        ['bar', '-', 0, 0],
                        ['foo', 1, '-', 0],
                        ['qux', 0, 0, '-'],
                    ],
                }

            def the_collection_must_exist(client, url):
                status, content = load(client.get(url))

                expect(status) == 404
