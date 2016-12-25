import logging

from flask import Blueprint, Response
from flask import request, render_template, redirect, url_for, flash
from flask_menu import register_menu

from .. import api

from ._utils import call


UNKNOWN_COLLECTION_NAME = "No Such Collection"

blueprint = Blueprint('admin', __name__)
log = logging.getLogger(__name__)


def _show_admin():
    parts = [p for p in request.path.split('/') if p]
    return len(parts) == 2 and parts[0] == 'collections'


@blueprint.route("/collections/<key>")
@register_menu(blueprint, '.admin', "Admin", order=1,
               visible_when=_show_admin)
def detail(key):
    content, status = call(api.collections.detail, key=key)
    if status == 404:
        content['name'] = UNKNOWN_COLLECTION_NAME
        content['items'] = []

    return Response(render_template("admin.html", collection=content))


@blueprint.route("/collections/<key>", methods=['POST'])
def update(key):
    log.critical(request.form)
    add = request.form.get('add', '').strip()
    remove = request.form.get('remove', '').strip()

    if add:
        _, status = call(api.items.add, key=key, name=add)
        assert status == 200

    if remove:
        _, status = call(api.items.remove, key=key, name=remove)
        assert status == 200

    return redirect(url_for('admin.detail', key=key))
