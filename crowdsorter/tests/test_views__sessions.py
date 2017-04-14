# pylint: disable=unused-variable,unused-argument,expression-not-assigned,singleton-comparison

from unittest.mock import patch

from expecter import expect

from crowdsorter.views import _session


class MockSession(dict):
    permanent = None


def describe_viewed_pairs():

    @patch('crowdsorter.views._session.session', MockSession())
    def it_defaults_to_an_empty_list():
        viewed_pairs = _session.get_viewed_pairs('mycode')

        expect(viewed_pairs) == []

    @patch('crowdsorter.views._session.session', MockSession())
    def it_retrieves_the_set_value():
        _session.set_viewed_pairs('mycode', [('foo', 'bar')])

        viewed_pairs = _session.get_viewed_pairs('mycode')

        expect(viewed_pairs) == [('foo', 'bar')]
