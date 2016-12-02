# from flask import url_for
from flask_api.exceptions import APIException


def call(function, *args, **kwargs):
    """Helper function to call the API internally."""
    try:
        content, status = function(*args, **kwargs)
    except APIException as exc:
        content = {'message': exc.detail}
        status = exc.status_code
    return content, status


def get_content(collection):
    """Serialize a collection for API responses."""
    content = collection.data
    # content['uri'] = url_for('api_collection.detail', _external=True)
    return content
