import logging
from urllib.error import HTTPError
import random

from flask import request, session
from flask_api.exceptions import APIException

from ..extensions import sendgrid


log = logging.getLogger(__name__)


def call(function, **kwargs):
    """Helper function to call the API internally."""
    try:
        request.data.update(kwargs)
        content, status = function(**kwargs)  # TODO: remove kwargs
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


def filter_pairs(content):
    """Filter previously viewed pairs and return the remaining percent."""
    key = content['code'] + '-pairs'
    viewed_pairs = session.get(key) or []
    names = content['items']
    total_pairs = len(names) * (len(names) - 1) / 2

    if len(viewed_pairs) >= total_pairs:
        return None, content

    next_pair = None
    while True:
        next_pair = names[0:2]
        next_pair.sort()

        if next_pair in viewed_pairs:
            random.shuffle(names)
            next_pair = None
        else:
            break

    if next_pair:
        viewed_pairs.append(next_pair)
        session[key] = viewed_pairs
        session.permanent = True

    percent = len(viewed_pairs) / total_pairs * 100
    content['items'] = names

    return percent, content
