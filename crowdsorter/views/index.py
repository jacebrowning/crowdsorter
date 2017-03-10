from flask import Blueprint, Response, render_template, url_for, current_app

from .. import api

from ._utils import call


blueprint = Blueprint('index', __name__)


@blueprint.route("/")
def get():
    content, status = call(api.collections.index, private=False, limit=3,
                           token=current_app.config['AUTH_TOKEN'])
    assert status == 200

    return Response(render_template("index.html",
                                    collections=content['_objects']))


@blueprint.route('/robots.txt')
def robots():
    excludes = [
        url_for('collections.index'),
    ]
    return Response(
        render_template("robots.txt", excludes=excludes),
        mimetype='text/plain',
    )
