# pylint: disable=unused-variable,unused-argument,expression-not-assigned,singleton-comparison

import pytest
from expecter import expect

from crowdsorter.models import Score, Scores


def describe_score():

    @pytest.fixture
    def score():
        return Score("Sample Item")

    def describe_repr():

        def it_includes_the_score(score):
            expect(repr(score)) == "<item: 'Sample Item' = 0.0 @ 0.0>"

    def describe_str():

        def it_uses_the_item(score):
            expect(str(score)) == "Sample Item"

    def describe_sort():

        def by_points():
            scores = [
                Score("a", _points=1.1),
                Score("b", _points=1.0),
                Score("c", _points=-10),
            ]

            expect(sorted(scores)) == scores

        def by_confidence():
            scores = [
                Score("a", _points=1, _confidence=0.9),
                Score("b", _points=1, _confidence=0.8),
                Score("c", _points=0.9),
            ]

            expect(sorted(scores)) == scores

    def describe_score2():

        @pytest.fixture
        def better():
            return Score("Better Item")

        @pytest.fixture
        def worse():
            return Score("Worse Item")

        @pytest.fixture
        def equal():
            return Score("Equal Item")

        def with_no_data(score):
            expect(score.score) == (0.0, 0.0)

        def with_1_win(score, worse):
            score.opponents = [worse]
            score.wins[worse] = 1

            expect(score.score) == (1.0, 1.0)

        def with_1_loss(score, better):
            score.opponents = [better]
            score.losses[better] = 1

            expect(score.score) == (-1.0, 1.0)

        def with_1_win_and_1_loss(score, better, worse):
            score.opponents = [better, worse]
            score.losses[better] = 1
            score.wins[worse] = 1

            score.losses[better] = 1

            expect(score.score) == (0.0, 1.0)

        def with_low_confidence_win(score, worse):
            score.opponents = [worse]
            score.wins[worse] = 3
            score.losses[worse] = 1

            expect(score.score) == (0.75, 0.75)

        def with_high_confidence_win(score, worse):
            score.opponents = [worse]
            score.wins[worse] = 99
            score.losses[worse] = 1

            expect(score.score) == (0.99, 0.99)

        def with_balanced_opponent(score, equal):
            score.opponents = [equal]
            score.wins[equal] = 42
            score.losses[equal] = 42

            expect(score.score) == (0.0, 0.0)

        def with_inferred_win(score, better, worse):
            better.opponents = [score, worse]
            score.opponents = [better, worse]
            better.wins[score] = 1
            score.wins[worse] = 1

            expect(better.score) == (1.9, 0.95)

        def with_inferred_loss(score, better, worse):
            worse.opponents = [score, better]
            score.opponents = [better, worse]
            worse.losses[score] = 1
            score.losses[better] = 1

            expect(worse.score) == (-1.9, 0.95)


def describe_scores():

    def describe_find():

        @pytest.fixture
        def scores():
            return Scores([Score("found")])

        def when_found(scores):
            expect(scores.find("found")) == Score("found")

        def when_missing(scores):
            expect(scores.find("missing")) == None

        def when_missing_with_creation(scores):
            expect(scores.find("missing", create=True)) == Score("missing")

    def describe_add_pair():

        @pytest.fixture
        def scores():
            return Scores.build(["b", "a", "c"])

        def when_transitive(scores):
            scores.add_pair("a", "b")
            scores.add_pair("b", "c")

            scores.sort()
            expect(scores) == [
                Score("a"),
                Score("b"),
                Score("c"),
            ]
