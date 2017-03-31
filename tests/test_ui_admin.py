# pylint: disable=unused-variable,unused-argument,redefined-outer-name,expression-not-assigned

from expecter import expect

from .utils import get, post


def describe_admin():

    def with_known_key(client, collection):
        html = get(client, "/collections/_c")

        expect(html).contains('<a href="/collections/_c">Admin</a>')
        expect(html).contains("Sample List")

    def with_unknown_key(client):
        html = get(client, "/collections/unknown")

        expect(html).contains("Not Found")

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

            expect(html).contains("Collection settings saved.")
            expect(html).contains('name="name" value="New Name"')

        def with_new_code(client, collection):
            data = dict(save=True, code="New Code")
            html = post(client, "/collections/_c", data)

            expect(html).contains("Collection settings saved.")
            expect(html).contains('name="code" value="new-code"')

        def with_duplicate_code(client, collection, collection2):
            data = dict(save=True, code="sample")
            html = post(client, "/collections/_c2", data)

            expect(html).contains("Short code is already taken: sample")

        def with_locked_set(client, collection):
            data = dict(save=True, unlocked=[])
            html = post(client, "/collections/_c", data)

            expect(html).contains("Collection settings saved.")
            expect(html).contains('name="unlocked"')

        def with_locked_clear(client, collection):
            data = dict(save=True, unlocked=['on'])
            html = post(client, "/collections/_c", data)

            expect(html).contains("Collection settings saved.")
            expect(html).contains('name="unlocked" checked=true')

        def with_private_set(client, collection):
            data = dict(save=True, public=[])
            html = post(client, "/collections/_c", data)

            expect(html).contains("Collection settings saved.")
            expect(html).contains('name="public"')

        def with_private_clear(client, collection):
            data = dict(save=True, public=['on'])
            html = post(client, "/collections/_c", data)

            expect(html).contains("Collection settings saved.")
            expect(html).contains('name="public" checked=true')

    def describe_add():

        def with_name(client, collection):
            data = dict(add="New Item")
            html = post(client, "/collections/_c", data)

            expect(html).contains("Added item: New Item")

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
            expect(html).contains("This is the admin page")

            html = get(client, "/sample")

            expect(html).contains("Votes: 0")

    def describe_delete():

        def it_redirects_to_the_collections_index(client, collection):
            data = dict(delete=True)
            html = post(client, "/collections/_c", data)

            expect(html).contains("Popular Collections")
            expect(html).does_not_contain('Sample List')
