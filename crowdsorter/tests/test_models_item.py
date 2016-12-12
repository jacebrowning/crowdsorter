# pylint: disable=unused-variable,unused-argument,expression-not-assigned,singleton-comparison

import pytest
from expecter import expect

from crowdsorter.models import Item


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
