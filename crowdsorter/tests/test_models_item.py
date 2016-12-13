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
            expect(repr(item)) == "Item('Sample Item', score=0.00)"

    def describe_str():

        def it_uses_the_name(item):
            expect(str(item)) == "Sample Item"

    def describe_sort():

        def it_uses_the_score():
            objs = [
                Item("a", score=42),
                Item("a", score=1),
                Item("a", score=0),
            ]


def describe_items():

    @pytest.fixture
    def items():
        green = Item("green")
        yellow = Item("yellow")
        blue = Item("blue")
        red = Item("red")
        green.wins = [yellow, blue, blue, blue]
        yellow.wins = [blue, red]
        blue.wins = [green, red]
        red.wins = []
        return Items([green, yellow, blue, red])

    def describe_tree():

        def it_lists_all_wins(items):
            expect(items.tree) == {
                "green": ["yellow", "blue", "blue", "blue"],
                "yellow": ["blue", "red"],
                "blue": ["green", "red"],
                "red": [],
            }

    def describe_find():

        def when_found(items):
            expect(items.find("blue")) == items[2]

        def when_missing(items):
            with expect.raises(IndexError):
                items.find("foobar")

    def describe_normalize():

        def it_removes_extra_win_loss_pairs(items):
            items.normalize()

            expect(items.tree) == {
                "green": ["yellow", "blue"],
                "yellow": ["blue", "red"],
                "blue": ["red"],
                "red": [],
            }
