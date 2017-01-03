import logging
from urllib.error import HTTPError

from flask import request
from flask_api.exceptions import APIException

from ..extensions import sendgrid


log = logging.getLogger(__name__)


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


def send_email(**kwargs):
    """Send an email using SendGrid."""
    try:
        response = sendgrid.send_email(**kwargs)
    except HTTPError as exc:
        log.exception(exc)
        response = None

    return response and 200 <= response.status_code < 300
