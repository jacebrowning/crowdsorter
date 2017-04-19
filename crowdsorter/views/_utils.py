import logging
from urllib.error import HTTPError
import random
import time
from pathlib import Path
import csv

from flask import request
from flask_api.exceptions import APIException

from ..extensions import sendgrid

from . import _session


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


def create_csv(filename, rows):
    root = Path('tmp').resolve()
    root.mkdir(parents=True, exist_ok=True)

    path = root.joinpath(filename)

    with path.open('w') as f:
        writer = csv.writer(f, lineterminator='\n')
        for row in rows:
            writer.writerow(row)

    return str(path)


def mark_pair_viewed(code, names):
    """Mark a pair as being viewed."""
    assert len(names) == 2

    _session.add_viewed_pair(code, sorted(names))


def mark_pair_voted(code, names):
    """Mark a pair as voted on."""
    for name in names:
        _session.add_voted_name(code, name)


def mark_pair_skipped(code, names):
    """Mark an item in a pair as skipped if the other has been voted."""
    assert len(names) == 2
    first, second = names

    voted_names = _session.get_voted_names(code)

    if first in voted_names:
        _session.add_skipped_name(code, second)

    if second in voted_names:
        _session.add_skipped_name(code, first)


def filter_voted_pairs(content):
    """Filter previously voted pairs and return the remaining percent."""
    code = content['code']
    items = list(filter_skipped_items(code, content['item_data']))
    total_pairs = len(items) * (len(items) - 1) / 2

    # Remove deleted pairs
    voted_pairs = []
    for pair in _session.get_viewed_pairs(code):
        found = True
        for name in pair:
            for item in items:
                if name == item['name']:
                    break
            else:
                found = False
        if found:
            voted_pairs.append(pair)

    # Exit if all pairs have been voted
    if len(voted_pairs) >= total_pairs:
        return None, content

    # Remove voted pairs and reshuffle items until a new pair is available
    next_pair = None
    start = time.time()
    while time.time() - start < 5:
        next_pair = sorted([items[0]['name'], items[1]['name']])

        if next_pair in voted_pairs:
            if len(items) > 2:
                items.pop(0)
            else:
                items = list(filter_skipped_items(code, content['item_data']))
                random.shuffle(items)
            next_pair = None
        else:
            break

    percent = len(voted_pairs) / total_pairs * 100
    content['item_data'] = items

    return percent, content


def filter_skipped_items(code, items):
    """Yield items that have not already been skipped."""
    skipped_names = _session.get_skipped_names(code)
    for item in items:
        if item['name'] in skipped_names:
            continue
        else:
            yield item


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
