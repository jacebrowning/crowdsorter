from flask import request
from flask_api.exceptions import APIException


def call(function, *args, **kwargs):
    """Helper function to call the API internally."""
    try:
        content, status = function(*args, **kwargs)
    except APIException as exc:
        content = {'message': exc.detail}
        status = exc.status_code
    return content, status


def parts():
    """Get the non-empty parts of the request path."""
    return [p for p in request.path.split('/') if p]
