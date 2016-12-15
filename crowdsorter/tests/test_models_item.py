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

        def with_no_data(item):
            expect(item.score) == (0.0, 0.0)

        def with_1_win(item, worse):
            item.win_count[worse] = 1

            expect(item.score) == (1.0, 1.0)

        def with_1_loss(item, better):
            item.loss_count[better] = 1

            expect(item.score) == (-1.0, 1.0)

        def with_1_win_and_1_loss(item, better, worse):
            item.loss_count[better] = 1
            item.win_count[worse] = 1

            item.loss_count[better] = 1

            expect(item.score) == (0.0, 1.0)

        def with_low_confidence_win(item, worse):
            item.win_count[worse] = 3
            item.loss_count[worse] = 1

            expect(item.score) == (0.5, 0.75)

        def with_high_confidence_win(item, worse):
            item.win_count[worse] = 99
            item.loss_count[worse] = 1

            expect(item.score) == (0.98, 0.99)


def describe_items():

    def describe_get_item():

        @pytest.fixture
        def items():
            return Items([Item("found")])

        def when_found(items):
            expect(items.get_item("found")) == Item("found")

        def when_missing(items):
            expect(items.get_item("missing")) == Item("missing")

    def describe_add_pair():

        @pytest.fixture
        def items():
            return Items()

        def when_transitive(items):
            items.add_pair("a", "b")
            items.add_pair("b", "c")

            expect(items.get_names()) == ["a", "b", "c"]
