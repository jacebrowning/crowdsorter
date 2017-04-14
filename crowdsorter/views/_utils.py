import logging
from urllib.error import HTTPError
import random
import time

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


def send_email(**kwargs):
    """Send an email using SendGrid."""
    try:
        response = sendgrid.send_email(**kwargs)
    except HTTPError as exc:
        log.exception(exc)
        response = None

    return response and 200 <= response.status_code < 300


def mark_pair_viewed(code, names):
    """Mark a pair as viewed."""
    key = code + '-pairs'
    viewed_pairs = session.get(key) or []

    assert len(names) == 2
    viewed_pair = sorted(names)

    viewed_pairs.append(viewed_pair)
    session[key] = viewed_pairs
    session.permanent = True


def filter_viewed_pairs(content):
    """Filter previously viewed pairs and return the remaining percent."""
    key = content['code'] + '-pairs'
    viewed_pairs = session.get(key) or []
    item_data = content['item_data'].copy()
    total_pairs = len(item_data) * (len(item_data) - 1) / 2
    viewed_pairs = []

    # Remove deleted pairs
    viewed_pairs = []
    for name_pair in session.get(key) or []:
        found = True
        for name in name_pair:
            for item in item_data:
                if name == item['name']:
                    break
            else:
                found = False
        if found:
            viewed_pairs.append(name_pair)

    # Exit if all pairs have been viewed
    if len(viewed_pairs) >= total_pairs:
        return None, content

    next_pair = None
    start = time.time()
    while time.time() - start < 5:
        next_pair = sorted([item_data[0]['name'], item_data[1]['name']])

        if next_pair in viewed_pairs:
            if len(item_data) > 2:
                item_data.pop(0)
            else:
                item_data = content['item_data'].copy()
                random.shuffle(item_data)
            next_pair = None
        else:
            break

    percent = len(viewed_pairs) / total_pairs * 100
    content['item_data'] = item_data

    return percent, content


def autoclose(seconds=2):
    """Automatically close unused target=_"blank" links."""
    template = """

    <!DOCTYPE html>
    <html>
    <body>

        <p>This window will close automatically...</p>

        <script type="text/javascript">
            setTimeout(function() {
                window.close();
            }, {milliseconds});
        </script>

    </body>
    </html>

    """.replace('  ', '').replace('\n', '')

    html = template.replace('{milliseconds}', str(seconds * 1000))

    return html, 400
