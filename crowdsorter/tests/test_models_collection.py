# pylint: disable=unused-variable,unused-argument,expression-not-assigned,singleton-comparison

import pytest
from expecter import expect

from crowdsorter.models import Collection


def describe_collection():

    @pytest.fixture
    def collection():
        return Collection(name="Sample List")

    def describe_init():

        def it_generates_a_unique_key():
            collection1 = Collection()
            collection2 = Collection()

            expect(collection1) != collection2

    def describe_sort():

        def it_sorts_by_key():
            objs = [
                Collection(key='1'),
                Collection(key='_'),
                Collection(key='a'),
            ]

            expect(sorted(objs)) == objs

    def describe_item_count():

        def is_the_number_of_items(collection):
            expect(collection.item_count) == 0

            collection.items.append("foobar")
            expect(collection.item_count) == 1

    def describe_vote_count():

        def is_the_number_of_votes(collection):
            expect(collection.vote_count) == 0

            collection.items = ["foo", "bar"]
            collection.vote("foo", "bar")
            expect(collection.vote_count) == 1
