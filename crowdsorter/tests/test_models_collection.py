# pylint: disable=unused-variable,unused-argument,expression-not-assigned,singleton-comparison

from datetime import datetime, timedelta

import pytest
from expecter import expect

from crowdsorter.models import Collection, Item


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

    def describe_vote_count():

        def is_the_number_of_votes(collection):
            expect(collection.vote_count) == 0

            collection.vote("foo", "bar")
            expect(collection.vote_count) == 1

    def describe_vote_count_decayed():

        def when_last_vote_is_now(collection):
            collection.vote("foo", "bar")

            expect(collection.vote_count_decayed) == 1.0

        def when_last_vote_is_recent(collection):
            dt = datetime.now() - timedelta(days=2)
            collection.vote("foo", "bar", _at=dt)

            expect(collection.vote_count_decayed) == 0.714

        def when_last_vote_is_old(collection):
            dt = datetime.now() - timedelta(days=21)
            collection.vote("foo", "bar", _at=dt)

            expect(collection.vote_count_decayed) == 0.0

        def when_last_vote_is_stale(collection):
            dt = datetime.now() - timedelta(days=99)
            collection.vote("foo", "bar", _at=dt)

            expect(collection.vote_count_decayed) == 0.0

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

        def it_decays_vote_count(collection):
            collection.vote("foo", "bar")
            collection.date_voted = collection.date_voted - timedelta(days=3)

            collection.clean()

            expect(collection.vote_count_decayed) == 0.571
