# pylint: disable=unused-variable,unused-argument,expression-not-assigned,singleton-comparison

import pytest
from expecter import expect

from crowdsorter.models import Collection, Item
from crowdsorter.models.collection import Wins, Loss, Score


def describe_collection():

    @pytest.fixture
    def collection():
        c = Collection(name="Sample List")
        c.items = [
            Item(name="foo"),
            Item(name="bar"),
        ]
        return c

    def describe_init():

        def it_generates_a_unique_key():
            collection1 = Collection()
            collection2 = Collection()

            expect(collection1.key) != collection2.key

    def describe_sort():

        def it_sorts_by_key():
            objs = [
                Collection(key='1'),
                Collection(key='_'),
                Collection(key='a'),
            ]

            expect(sorted(objs)) == objs

    def describe_contains():

        def it_checks_for_items_in_collection(collection):
            item_in = collection.items[0]
            item_out = Item()

            expect(collection).contains(item_in)
            expect(collection).does_not_contain(item_out)

    def describe_item_count():

        def is_the_number_of_items(collection):
            expect(collection.item_count) == 2

            collection.items.append(Item(name="foobar"))
            expect(collection.item_count) == 3

    def describe_vote_count():

        def is_the_number_of_votes(collection):
            expect(collection.vote_count) == 0

            collection.vote("foo", "bar")
            expect(collection.vote_count) == 1

    def describe_add():

        def it_creates_an_item(collection):
            item = collection.add("New Item", _save=False)

            expect(item.name) == collection.items[-1].name

    def describe_clean():

        def it_generates_a_unique_code():
            collection1 = Collection()
            collection2 = Collection()
            collection1.clean()
            collection2.clean()

            expect(collection1.code) != collection2.code
