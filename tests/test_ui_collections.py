# pylint: disable=unused-variable,unused-argument,redefined-outer-name,expression-not-assigned

from expecter import expect

from .utils import get, post


def describe_collections():

    def describe_index():

        def with_collections(client, collection):
            html = get(client, "/collections/")

            expect(html).contains("Popular Collections")
            expect(html).contains('<a href="/sample" class="list-group-item">')
            expect(html).contains("1 Votes")

        def describe_search():

            def when_collections_found(client, collection):
                html = get(client, "/collections/?q=samp")

                expect(html).contains("Clear search results")
                expect(html).contains("Sample List")

            def when_no_results(client, collection):
                html = get(client, "/collections/?q=foobar")

                expect(html).contains("Clear search results")
                expect(html).contains("No matching collections found.")

        def describe_new():

            def with_name(client):
                data = {'name': "My List"}
                html = post(client, "/collections/", data)

                expect(html).contains("My List")
                expect(html).contains("This is the admin page")

            def without_name(client):
                data = {}
                html = post(client, "/collections/", data)

                expect(html).contains("A name is required.")
