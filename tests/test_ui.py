# pylint: disable=unused-variable,unused-argument,redefined-outer-name,expression-not-assigned

from datetime import datetime

from expecter import expect

from .utils import get


def describe_navbar():

    def for_index(client):
        html = get(client, "/", minify=True)

        expect(html).contains('<li>'
                              '<a href="/collections/">Collections</a>')

    def for_collections(client):
        html = get(client, "/collections", minify=True)

        expect(html).contains('<li class="active">'
                              '<a href="/collections/">Collections</a>')

    def for_admin(client, collection):
        html = get(client, "/collections/_c", minify=True)

        expect(html).contains('<li>'
                              '<a href="/collections/">Collections</a>')
        expect(html).contains('<li class="active">'
                              '<a href="/collections/_c">Admin</a>')

    def for_results(client, collection):
        html = get(client, "/sample", minify=True)

        expect(html).contains('<li>'
                              '<a href="/collections/">Collections</a>')
        expect(html).contains('<li class="active">'
                              '<a href="/sample">Results</a>')
        expect(html).contains('<li>'
                              '<a href="/sample/vote">Vote</a>')

    def for_vote(client, collection):
        html = get(client, "/sample/vote", minify=True)

        expect(html).contains('<li>'
                              '<a href="/collections/">Collections</a>')
        expect(html).contains('<li>'
                              '<a href="/sample">Results</a>')
        expect(html).contains('<li class="active">'
                              '<a href="/sample/vote">Vote</a>')


def describe_footer():

    def it_contains_the_year(client):
        year = str(datetime.now().year)
        html = get(client, "/")

        expect(html).contains(year)


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


def describe_static():

    def when_missing(client):
        html = get(client, "/static/images/missing.png")

        expect(html).contains("Not Found")
