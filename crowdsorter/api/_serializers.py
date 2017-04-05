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


def serialize_redirect(redirect):
    return dict(
        _links=dict(
            self=url_for('redirects_api.detail',
                         start_slug=redirect.start_slug, _external=True),
            index=url_for('redirects_api.index', _external=True),
        ),
        start_slug=redirect.start_slug,
        end_slug=redirect.end_slug,
    )
