# pylint: disable=wildcard-import,unused-wildcard-import

from flask_api.exceptions import *


class UnprocessableEntity(APIException):
    status_code = 422
    detail = "Unable to process the request."
