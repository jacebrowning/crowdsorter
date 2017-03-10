from flask import url_for


def serialize_item(item):
    return dict(
        _links=dict(
            self=url_for('items_api.detail', key=item.key, _external=True),
        ),
        key=item.key,
        name=item.name,
        description=item.description or "",
        image_url=item.image_url or "",
        ref_url=item.ref_url or "",
    )
