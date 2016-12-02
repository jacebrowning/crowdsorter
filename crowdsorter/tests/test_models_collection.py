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
