# pylint: disable=unused-variable,unused-argument,expression-not-assigned,singleton-comparison

import pytest
from expecter import expect

from crowdsorter.models import Item, Items


def describe_item():

    @pytest.fixture
    def item():
        return Item("Sample Item")

    def describe_repr():

        def it_includes_the_score(item):
            expect(repr(item)) == "<item: 'Sample Item' = 0.0 @ 0.0>"

    def describe_str():

        def it_uses_the_name(item):
            expect(str(item)) == "Sample Item"

    def describe_sort():

        def by_points():
            items = [
                Item("a", _points=1.1),
                Item("b", _points=1.0),
                Item("c", _points=-10),
            ]

            expect(sorted(items)) == items

        def by_confidence():
            items = [
                Item("a", _points=1, _confidence=0.9),
                Item("b", _points=1, _confidence=0.8),
                Item("c", _points=0.9),
            ]

            expect(sorted(items)) == items

    def describe_score():

        @pytest.fixture
        def better():
            return Item("Better Item")

        @pytest.fixture
        def worse():
            return Item("Worse Item")

        @pytest.fixture
        def equal():
            return Item("Equal Item")

        def with_no_data(item):
            expect(item.score) == (0.0, 0.0)

        def with_1_win(item, worse):
            item.opponents = [worse]
            item.wins[worse] = 1

            expect(item.score) == (1.0, 1.0)

        def with_1_loss(item, better):
            item.opponents = [better]
            item.losses[better] = 1

            expect(item.score) == (-1.0, 1.0)

        def with_1_win_and_1_loss(item, better, worse):
            item.opponents = [better, worse]
            item.losses[better] = 1
            item.wins[worse] = 1

            item.losses[better] = 1

            expect(item.score) == (0.0, 1.0)

        def with_low_confidence_win(item, worse):
            item.opponents = [worse]
            item.wins[worse] = 3
            item.losses[worse] = 1

            expect(item.score) == (0.75, 0.75)

        def with_high_confidence_win(item, worse):
            item.opponents = [worse]
            item.wins[worse] = 99
            item.losses[worse] = 1

            expect(item.score) == (0.99, 0.99)

        def with_balanced_opponent(item, equal):
            item.opponents = [equal]
            item.wins[equal] = 42
            item.losses[equal] = 42

            expect(item.score) == (0.0, 0.0)

        def with_inferred_win(item, better, worse):
            better.opponents = [item, worse]
            item.opponents = [better, worse]
            better.wins[item] = 1
            item.wins[worse] = 1

            expect(better.score) == (1.99, 0.75)

        def with_inferred_loss(item, better, worse):
            worse.opponents = [item, better]
            item.opponents = [better, worse]
            worse.losses[item] = 1
            item.losses[better] = 1

            expect(worse.score) == (-1.99, 0.75)


def describe_items():

    def describe_find():

        @pytest.fixture
        def items():
            return Items([Item("found")])

        def when_found(items):
            expect(items.find("found")) == Item("found")

        def when_missing(items):
            expect(items.find("missing")) == None

        def when_missing_with_creation(items):
            expect(items.find("missing", create=True)) == Item("missing")

    def describe_add_pair():

        @pytest.fixture
        def items():
            return Items.build(["b", "a", "c"])

        def when_transitive(items):
            items.add_pair("a", "b")
            items.add_pair("b", "c")

            items.sort()
            expect(items) == [
                Item("a"),
                Item("b"),
                Item("c"),
            ]
