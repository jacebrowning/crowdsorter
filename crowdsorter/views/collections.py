from flask import Blueprint, Response, render_template, redirect, url_for

from .. import api

from ._utils import call


blueprint = Blueprint('collections', __name__)


@blueprint.route("/collections/")
def index():
    return redirect(url_for('index.get'))


@blueprint.route("/collections/<key>")
def detail(key):
    content, status = call(api.collections.detail, key=key)

    assert status == 200

    return Response(render_template("collection.html", collection=content))


@blueprint.route("/collections/<key>/items")
def items(key):
    content, status = call(api.collections.detail, key=key)

    assert status == 200

    return Response(render_template("items.html", collection=content))


@blueprint.route("/collections/<key>/sort")
def sort(key):
    content, status = call(api.collections.detail, key=key)

    assert status == 200

    return Response(render_template("sort.html", collection=content))
