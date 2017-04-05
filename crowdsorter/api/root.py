import logging

from flask import Blueprint, url_for, redirect
from flask_api import status


blueprint = Blueprint('root_api', __name__)
log = logging.getLogger(__name__)


@blueprint.route("/api")
def index():
    content = dict(
        _links=dict(
            self=url_for('.index', _external=True),
            collections=url_for('collections_api.index', _external=True),
            redirects=url_for('redirects_api.index', _external=True),
        ),
    )

    return content, status.HTTP_200_OK


@blueprint.route("/api/")
def redirect_to_index():
    return redirect(url_for('.index'))
