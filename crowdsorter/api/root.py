import logging

from flask import Blueprint, url_for
from flask_api import status


blueprint = Blueprint('root_api', __name__)
log = logging.getLogger(__name__)


@blueprint.route("/api")
def index():
    content = {'collections': url_for('collections_api.index', _external=True)}

    return content, status.HTTP_200_OK
