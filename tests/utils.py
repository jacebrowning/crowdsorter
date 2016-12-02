
import json
import logging
from typing import Union

import flask

log = logging.getLogger(__name__)


def load(response: flask.Response) -> (int, Union[dict, str]):
    """Convert a response's binary data (JSON) to a dictionary."""
    text = response.data.decode('utf-8')

    if text:
        try:
            data = json.loads(text)
        except json.decoder.JSONDecodeError:
            data = text
    else:
        data = None

    log.debug("Response: %r", data)

    return response.status_code, data


def get(client, url):
    """Simulate loading a page."""
    log.debug("GET request URL: %s", url)
    response = client.get(url, follow_redirects=True)

    html = response.data.decode('utf-8')

    log.debug("Response HTML: \n\n%s\n", html)

    return html


def post(client, url, data):
    """Simulate a form submission on a page."""
    log.debug("POST request URL: %s", url)
    log.debug("with data: %s", data)
    response = client.post(url, data=data, follow_redirects=True)

    html = response.data.decode('utf-8')

    log.debug("Response HTML: \n\n%s\n", html)

    return html
