import logging

from flask import Blueprint, Response
from flask import request, flash, url_for, render_template, redirect, abort

from .. import api

from ._utils import call


blueprint = Blueprint('items', __name__, url_prefix="/items")
log = logging.getLogger(__name__)


@blueprint.route("/<key>")
def detail(key):
    content, status = call(api.items.detail, key=key)

    if status != 200:
        abort(404)

    return Response(render_template("item.html", item=content))


@blueprint.route("/<key>", methods=['POST'])
def update(key):
    data = dict(
        name=request.form.get('name') or None,
        description=request.form.get('description') or None,
        image_url=request.form.get('image_url') or None,
        ref_url=request.form.get('ref_url') or None,
    )
    log.debug("Form values: %s", data)

    content, status = call(api.items.update, key=key, **data)

    if status == 200:
        flash("Item properties updated.", 'info')
    else:
        flash(content['message'], 'danger')

    return redirect(url_for('items.detail', key=key))
