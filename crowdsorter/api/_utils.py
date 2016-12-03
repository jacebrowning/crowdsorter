# from flask import url_for


def get_content(collection):
    """Serialize a collection for API responses."""
    content = collection.data
    # content['uri'] = url_for('api_collection.detail', _external=True)
    return content
