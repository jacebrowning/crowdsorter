from collections import OrderedDict

from flask import url_for


def get_content(collection):
    """Serialize a collection for API responses."""
    content = OrderedDict()

    content['uri'] = url_for('collections_api.detail',
                             key=collection.key, _external=True)
    content['name'] = collection.name
    content['items'] = collection.items

    return content
