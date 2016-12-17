# pylint: disable=unused-variable,unused-argument,expression-not-assigned,singleton-comparison

import pytest
from expecter import expect

from crowdsorter.models import Collection
from crowdsorter.models.collection import Wins, Loss, Score


def describe_collection():

    @pytest.fixture
    def collection():
        c = Collection(name="Sample List")
        c.items = ["foo", "bar"]
        return c

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
            expect(collection.item_count) == 2

            collection.items.append("foobar")
            expect(collection.item_count) == 3

    def describe_vote_count():

        def is_the_number_of_votes(collection):
            expect(collection.vote_count) == 0

            collection.vote("foo", "bar")
            expect(collection.vote_count) == 1

    def describe_clean():

        def it_removes_stale_votes(collection):
            collection.vote("foo", "bar")
            collection.vote("foo", "unknown")
            collection.vote("unknown", "bar")
            assert collection.votes == [
                Wins(winner="foo", against=[
                    Loss(loser="bar", count=1),
                    Loss(loser="unknown", count=1),
                ]),
                Wins(winner="unknown", against=[
                    Loss(loser="bar", count=1),
                ]),
            ]
            assert collection.scores == []

            collection.clean()

            expect(collection.votes) == [
                Wins(winner="foo", against=[
                    Loss(loser="bar", count=1),
                ]),
                Wins(winner="bar", against=[
                    Loss(loser="foo", count=0),
                ]),
            ]
            expect(collection.scores) == [
                Score(name="foo", points=1.0, confidence=1.0),
                Score(name="bar", points=-1.0, confidence=1.0),
            ]
