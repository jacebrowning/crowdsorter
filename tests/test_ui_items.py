# pylint: disable=unused-variable,unused-argument,redefined-outer-name,expression-not-assigned

import pytest
from expecter import expect

from .utils import get, post


def describe_items():

    @pytest.fixture
    def url():
        return "/items/_i"

    def with_known_key(client, url, item):
        html = get(client, url)

        expect(html).contains("Sample Item")

    def with_unknown_key(client):
        html = get(client, "/items/unknown")

        expect(html).contains("Not Found")

    def describe_save():

        def with_new_name(client, url, item):
            data = dict(save=True, name="New Name")
            html = post(client, url, data)

            expect(html).contains("Item properties saved.")
            expect(html).contains('<b>New Name</b>')

        def with_new_image_url(client, url, item):
            data = dict(save=True, image_url="http://example.com/image.jpg")
            html = post(client, url, data)

            expect(html).contains("Item properties saved.")
            expect(html).contains('<img src="http://example.com/image.jpg"')

        def with_new_description(client, url, item):
            data = dict(save=True, description="New description.")
            html = post(client, url, data)

            expect(html).contains("Item properties saved.")
            expect(html).contains('<p>New description.</p>')

        def with_new_ref_url(client, url, item):
            data = dict(save=True, ref_url="http://example.com")
            html = post(client, url, data)

            expect(html).contains("Item properties saved.")
            expect(html).contains('<a href="http://example.com"')

        def with_bad_image_url(client, url, item):
            data = dict(save=True, image_url="http://bad/image.jpg")
            html = post(client, url, data)

            expect(html).contains("Invalid URL: http://bad/image.jpg")

        def with_bad_ref_url(client, url, item):
            data = dict(save=True, ref_url="http://bad/ref")
            html = post(client, url, data)

            expect(html).contains("Invalid URL: http://bad/ref")

    def describe_delete():

        def it_closes_the_window(client, url, item):
            data = dict(delete=True)
            html = post(client, url, data)

            expect(html).contains('window.close()')
