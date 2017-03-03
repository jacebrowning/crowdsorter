# pylint: disable=unused-variable,unused-argument,expression-not-assigned,singleton-comparison

import pytest
from expecter import expect

from crowdsorter.models import Item


def describe_item():

    @pytest.fixture
    def item():
        i = Item(name="Sample Item")
        return i

    def describe_init():

        def it_generates_a_unique_key():
            item1 = Item()
            item2 = Item()

            expect(item1.key) != item2.key

    def describe_str():

        def it_uses_the_name(item):
            expect(str(item)) == "Sample Item"
