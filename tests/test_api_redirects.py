# pylint: disable=unused-variable,unused-argument,expression-not-assigned,singleton-comparison

import pytest
from expecter import expect

from .utils import load


def describe_items():

    def describe_index():

        @pytest.fixture
        def url():
            return "/api/redirects/"

        def describe_GET():

            def it_requires_auth(client, url, redirect):
                status, content = load(client.get(url))

                expect(status) == 403

            def it_returns_a_list_of_redirects(client, url, redirect):
                status, content = load(client.get(url + "?token=test"))

                expect(status) == 200
                expect(content) == {
                    '_links': {
                        'root': "http://localhost/api",
                        'self': "http://localhost/api/redirects/",
                    },
                    '_objects': [
                        {
                            '_links': {
                                'self': "http://localhost/api/redirects/old",
                                'index': "http://localhost/api/redirects/",
                            },
                            'start_slug': "old",
                            'end_slug': "sample",
                        },
                    ],

                }

        def describe_POST():

            def it_creates_a_new_redirect(client, url):
                data = {'start_slug': "start", 'end_slug': "end"}
                status, content = load(client.post(url, data=data))

                expect(status) == 201
                expect(content['start_slug']) == "start"
                expect(content['end_slug']) == "end"

            def it_requires_start_and_end_slugs(client, url):
                status, content = load(client.post(url))

                expect(status) == 422
                expect(content['message']).contains(" are required.")

    def describe_detail():

        @pytest.fixture
        def url():
            return "/api/redirects/old"

        def describe_GET():

            def it_returns_a_new_slug(client, url, redirect):
                status, content = load(client.get(url))

                expect(status) == 200
                expect(content) == {
                    '_links': {
                        'self': "http://localhost/api/redirects/old",
                        'index': "http://localhost/api/redirects/",
                    },
                    'start_slug': "old",
                    'end_slug': "sample",
                }

            def when_unknown(client):
                status, content = load(client.get("/api/redirects/unknown"))

                expect(status) == 404

        def describe_PUT():

            def it_can_update_the_slug(client, url, redirect):
                data = {'end_slug': "my new Name "}
                status, content = load(client.put(url, data=data))

                expect(status) == 200
                expect(content['end_slug']) == "my-new-name"

            def it_fails_on_empty_slugs(client, url, redirect):
                data = {'end_slug': "  "}
                status, content = load(client.put(url, data=data))

                expect(status) == 422

            def when_unknown(client):
                url = "/api/redirects/unknown"
                data = {'end_slug': "my new Name "}
                status, content = load(client.put(url, data=data))

                expect(status) == 404
