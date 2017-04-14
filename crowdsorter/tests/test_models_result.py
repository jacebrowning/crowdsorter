# pylint: disable=unused-variable,unused-argument,expression-not-assigned,singleton-comparison

import pytest
from expecter import expect

from crowdsorter.models import Result, Results


def describe_result():

    @pytest.fixture
    def result():
        return Result("Sample Item")

    def describe_repr():

        def it_includes_the_result(result):
            expect(repr(result)) == "<item: 'Sample Item' = 0.000 @ 0.000>"

    def describe_str():

        def it_uses_the_item(result):
            expect(str(result)) == "Sample Item"

    def describe_sort():

        def by_points():
            results = [
                Result("a", _points=1.1),
                Result("b", _points=1.0),
                Result("c", _points=-10),
            ]

            expect(sorted(results)) == results

        def by_confidence():
            results = [
                Result("a", _points=1, _confidence=0.9),
                Result("b", _points=1, _confidence=0.8),
                Result("c", _points=0.9),
            ]

            expect(sorted(results)) == results

    def describe_inferred_points_impact():

        def when_0_opponents(result):
            result.opponents = []

            expect(result.inferred_points_impact) == 0

        def when_1_opponent(result):
            result.opponents = ['b']

            expect(result.inferred_points_impact) == 0

        def when_2_opponents(result):
            result.opponents = ['b', 'c']

            expect(result.inferred_points_impact) == 1 / 1

        def when_3_opponents(result):
            result.opponents = ['b', 'c', 'd']

            expect(result.inferred_points_impact) == 1 / 3

        def when_4_opponents(result):
            result.opponents = ['b', 'c', 'd', 'e']

            expect(result.inferred_points_impact) == 1 / 6

    def describe_score():

        @pytest.fixture
        def better():
            return Result("Better Item")

        @pytest.fixture
        def worse():
            return Result("Worse Item")

        @pytest.fixture
        def equal():
            return Result("Equal Item")

        def with_no_data(result):
            expect(result.score) == (0.0, 0.0)

        def with_1_win(result, worse):
            result.opponents = [worse]
            result.wins[worse] = 1

            expect(result.score) == (1.0, 1.0)

        def with_1_loss(result, better):
            result.opponents = [better]
            result.losses[better] = 1

            expect(result.score) == (-1.0, 1.0)

        def with_1_win_and_1_loss(result, better, worse):
            result.opponents = [better, worse]
            result.losses[better] = 1
            result.wins[worse] = 1

            result.losses[better] = 1

            expect(result.score) == (0.0, 1.0)

        def with_low_confidence_win(result, worse):
            result.opponents = [worse]
            result.wins[worse] = 3
            result.losses[worse] = 1

            expect(result.score) == (0.75, 0.75)

        def with_high_confidence_win(result, worse):
            result.opponents = [worse]
            result.wins[worse] = 99
            result.losses[worse] = 1

            expect(result.score) == (0.99, 0.99)

        def with_balanced_opponent(result, equal):
            result.opponents = [equal]
            result.wins[equal] = 42
            result.losses[equal] = 42

            expect(result.score) == (0.0, 0.0)

        def with_inferred_win(result, better, worse):
            better.opponents = [result, worse]
            result.opponents = [better, worse]
            better.wins[result] = 1
            result.wins[worse] = 1

            expect(better.score) == (2.0, 2 / 3)

        def with_inferred_loss(result, better, worse):
            worse.opponents = [result, better]
            result.opponents = [better, worse]
            worse.losses[result] = 1
            result.losses[better] = 1

            expect(worse.score) == (-2.0, 2 / 3)


def describe_results():

    def describe_find():

        @pytest.fixture
        def results():
            return Results([Result("found")])

        def when_found(results):
            expect(results.find("found")) == Result("found")

        def when_missing(results):
            expect(results.find("missing")) == None

        def when_missing_with_creation(results):
            expect(results.find("missing", create=True)) == Result("missing")

    def describe_add_pair():

        @pytest.fixture
        def results():
            return Results.build(["b", "a", "c"])

        def when_transitive(results):
            results.add_pair("a", "b")
            results.add_pair("b", "c")

            results.sort()
            expect(results) == [
                Result("a"),
                Result("b"),
                Result("c"),
            ]
