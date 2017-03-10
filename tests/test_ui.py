# pylint: disable=unused-variable,unused-argument,redefined-outer-name,expression-not-assigned

import pytest
from expecter import expect

from .utils import get, post


def describe_navbar():

    def for_index(client):
        html = get(client, "/", minify=True)

        expect(html).contains('<li>'
                              '<a href="/collections/">Collections</a>')

    def for_collections(client):
        html = get(client, "/collections", minify=True)

        expect(html).contains('<li class="active">'
                              '<a href="/collections/">Collections</a>')

    def for_admin(client):
        html = get(client, "/collections/_c", minify=True)

        expect(html).contains('<li>'
                              '<a href="/collections/">Collections</a>')
        expect(html).contains('<li class="active">'
                              '<a href="/collections/_c">Admin</a>')

    def for_results(client):
        html = get(client, "/foobar", minify=True)

        expect(html).contains('<li>'
                              '<a href="/collections/">Collections</a>')
        expect(html).contains('<li class="active">'
                              '<a href="/foobar">Results</a>')
        expect(html).contains('<li>'
                              '<a href="/foobar/vote">Vote</a>')

    def for_vote(client):
        html = get(client, "/foobar/vote", minify=True)

        expect(html).contains('<li>'
                              '<a href="/collections/">Collections</a>')
        expect(html).contains('<li>'
                              '<a href="/foobar">Results</a>')
        expect(html).contains('<li class="active">'
                              '<a href="/foobar/vote">Vote</a>')


def describe_index():

    def it_contains_link_to_sample_collection(client):
        html = get(client, "/")

        expect(html).contains('href="/collections/"')

    def for_robots(client):
        text = get(client, "/robots.txt")

        expect(text) == (
            "User-agent: *" + '\n'
            "Disallow: /collections/" + '\n'
        )


def describe_collections():

    def describe_index():

        def with_collections(client, collection):
            html = get(client, "/collections/")

            expect(html).contains("Popular Collections")
            expect(html).contains('<a href="/sample" class="list-group-item">')
            expect(html).contains("1 Votes")

        def describe_new():

            def with_name(client):
                data = {'name': "My List"}
                html = post(client, "/collections/", data)

                expect(html).contains("Created collection: My List")
                expect(html).contains("My List")

            def without_name(client):
                data = {}
                html = post(client, "/collections/", data)

                expect(html).contains("A name is required.")

    def describe_items():

        def with_known_code(client, collection):
            html = get(client, "/sample")

            expect(html).contains('<a href="/sample">Results</a>')
            expect(html).contains('<a href="/sample/vote">Vote</a>')
            expect(html).contains("Sample List")
            expect(html).contains("Items: 3")
            expect(html).contains('glyphicon-plus-sign')
            expect(html).contains("Share on Facebook")

        def with_unknown_code(client, collection):
            html = get(client, "/unknown")

            expect(html).contains("No Such Collection")
            expect(html).contains("Items: 0")
            expect(html).does_not_contain('glyphicon-plus-sign')
            expect(html).does_not_contain("Share on Facebook")

        def on_private_collection(client, collection_private):
            html = get(client, "/sample")

            expect(html).does_not_contain("Share on Facebook")

        def describe_add():

            def with_name(client, collection):
                data = dict(name="New Item")
                html = post(client, "/sample", data)

                expect(html).contains('<h2 class="title">New Item</h2>')

            def on_locked_collection(client, collection_locked):
                data = dict(name="New Item")
                html = post(client, "/sample", data)

                expect(html).contains("This window will close automatically...")

    def describe_votes():

        def with_known_code(client, collection):
            html = get(client, "/sample/vote")

            expect(html).contains('<a href="/sample">Results</a>')
            expect(html).contains('<a href="/sample/vote">Vote</a>')
            expect(html).contains("Sample List")
            expect(html).contains("New Comparison Pair")

        def with_unknown_code(client):
            html = get(client, "/unknown/vote")

            expect(html).contains("No Such Collection")


def describe_admin():

    def with_known_key(client, collection):
        html = get(client, "/collections/_c")

        expect(html).contains('<a href="/collections/_c">Admin</a>')
        expect(html).contains("Sample List")

    def with_unknown_key(client):
        html = get(client, "/collections/unknown")

        expect(html).contains("No Such Collection")

    def describe_email():
        """None of these tests can actually send an email."""

        def with_new_address(client, collection):
            data = dict(email="foo@bar.com")
            html = post(client, "/collections/_c", data)

            expect(html).contains("Unable to send email: foo@bar.com")
            expect(html).contains('name="email" value="foo@bar.com"')

        def with_invalid_address(client, collection):
            data = dict(email="foobar")
            html = post(client, "/collections/_c", data)

            expect(html).contains("Invalid email address: foobar")
            expect(html).contains('name="email" value=""')

    def describe_save():

        def with_new_name(client, collection):
            data = dict(save=True, name="New Name")
            html = post(client, "/collections/_c", data)

            expect(html).contains("Settings updated.")
            expect(html).contains('name="name" value="New Name"')

        def with_new_code(client, collection):
            data = dict(save=True, code="New Code")
            html = post(client, "/collections/_c", data)

            expect(html).contains("Settings updated.")
            expect(html).contains('name="code" value="new-code"')

        def with_duplicate_code(client, collection, collection2):
            data = dict(save=True, code="sample")
            html = post(client, "/collections/_c2", data)

            expect(html).contains("Short code is already taken: sample")

        def with_locked_set(client, collection):
            data = dict(save=True, unlocked=[])
            html = post(client, "/collections/_c", data)

            expect(html).contains("Settings updated.")
            expect(html).contains('name="unlocked"')

        def with_locked_clear(client, collection):
            data = dict(save=True, unlocked=['on'])
            html = post(client, "/collections/_c", data)

            expect(html).contains("Settings updated.")
            expect(html).contains('name="unlocked" checked=true')

        def with_private_set(client, collection):
            data = dict(save=True, public=[])
            html = post(client, "/collections/_c", data)

            expect(html).contains("Settings updated.")
            expect(html).contains('name="public"')

        def with_private_clear(client, collection):
            data = dict(save=True, public=['on'])
            html = post(client, "/collections/_c", data)

            expect(html).contains("Settings updated.")
            expect(html).contains('name="public" checked=true')

    def describe_add():

        def with_name(client, collection):
            data = dict(add="New Item")
            html = post(client, "/collections/_c", data)

            expect(html).contains("Added item: New Item")
            expect(html).contains('value="New Item" name="remove"')

    def describe_remove():

        def with_name(client, collection):
            data = dict(remove="foo")
            html = post(client, "/collections/_c", data)

            expect(html).contains("Removed item: foo")
            expect(html).does_not_contain('value="foo" name="remove"')

    def describe_view():

        def it_redirects(client, collection):
            data = dict(view=True)
            html = post(client, "/collections/_c", data)

            expect(html).contains("Votes: 1")

    def describe_clear():

        def it_clears_votes(client, collection):
            data = dict(clear=True)
            html = post(client, "/collections/_c", data)

            expect(html).contains("Votes cleared.")
            expect(html).contains('<a href="/collections/_c">Admin</a>')

            html = get(client, "/sample")

            expect(html).contains("Votes: 0")

    def describe_delete():

        def it_redirects_to_the_collections_index(client, collection):
            data = dict(delete=True)
            html = post(client, "/collections/_c", data)

            expect(html).contains("Popular Collections")
            expect(html).does_not_contain('Sample List')


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

            expect(html).contains("Item properties updated.")
            expect(html).contains('<b>New Name</b>')

        def with_new_image_url(client, url, item):
            data = dict(save=True, image_url="http://example.com/image.jpg")
            html = post(client, url, data)

            expect(html).contains("Item properties updated.")
            expect(html).contains('<img src="http://example.com/image.jpg"')

        def with_new_description(client, url, item):
            data = dict(save=True, description="New description.")
            html = post(client, url, data)

            expect(html).contains("Item properties updated.")
            expect(html).contains('<p>New description.</p>')

        def with_new_ref_url(client, url, item):
            data = dict(save=True, ref_url="http://example.com")
            html = post(client, url, data)

            expect(html).contains("Item properties updated.")
            expect(html).contains('<a href="http://example.com"')

        def with_bad_image_url(client, url, item):
            data = dict(save=True, image_url="http://bad/image.jpg")
            html = post(client, url, data)

            expect(html).contains("Invalid URL: http://bad/image.jpg")

        def with_bad_ref_url(client, url, item):
            data = dict(save=True, ref_url="http://bad/ref")
            html = post(client, url, data)

            expect(html).contains("Invalid URL: http://bad/ref")
