import logging

from flask import Blueprint
from flask_api import status

# from ..models import Collection

# from . import _exceptions as exceptions
# from ._utils import get_content


blueprint = Blueprint('api_collections', __name__,
                      url_prefix="/api/collections")
log = logging.getLogger(__name__)


@blueprint.route("/")
def index():
    return [], status.HTTP_200_OK
