# pylint: disable=wildcard-import,unused-wildcard-import

from mongoengine.errors import *
from flask_api.exceptions import *


class UnprocessableEntity(APIException):
    status_code = 422
    detail = "Unable to process the request."


class Conflict(APIException):
    status_code = 409
