from collections import OrderedDict

from flask import url_for


def get_content(collection):
    """Serialize a collection for API responses."""
    content = OrderedDict()

    content['uri'] = url_for('collections_api.detail',
                             key=collection.key, _external=True)
    content['key'] = collection.key
    content['name'] = collection.name
    content['code'] = collection.code
    content['items'] = sorted(collection.items)

    return content
