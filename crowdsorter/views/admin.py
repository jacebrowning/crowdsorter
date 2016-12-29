import logging

from flask import Blueprint, Response
from flask import request, render_template, redirect, url_for, flash
from flask_menu import register_menu

from .. import api

from ._utils import call, parts


UNKNOWN_COLLECTION_NAME = "No Such Collection"

blueprint = Blueprint('admin', __name__)
log = logging.getLogger(__name__)


def _show_admin():
    return len(parts()) == 2 and parts()[0] == 'collections'


@blueprint.route("/collections/<key>")
@register_menu(blueprint, '.admin', "Admin", order=2,
               visible_when=_show_admin)
def detail(key):
    content, status = call(api.collections.detail, key=key)
    if status == 404:
        content['name'] = UNKNOWN_COLLECTION_NAME
        content['items'] = []

    return Response(render_template("admin.html", collection=content))


@blueprint.route("/collections/<key>", methods=['POST'])
def update(key):
    name = request.form.get('name')
    code = request.form.get('code')
    private = not request.form.getlist('public')
    locked = not request.form.getlist('unlocked')
    save = request.form.get('save')
    add = request.form.get('add', '').strip()
    remove = request.form.get('remove', '').strip()
    log.debug(f"Form options: private={private} locked={locked}")
    log.debug(f"Form actions: save={save} add={add} remove={remove}")

    if save:
        content, status = call(api.collections.update, key=key,
                               name=name, code=code,
                               private=private, locked=locked)
        if status == 200:
            flash("Settings updated.", 'info')
        else:
            flash(content['message'], 'danger')

    if add:
        _, status = call(api.items.add, key=key, name=add)
        assert status == 200
        flash(f"Added item: {add}", 'info')

    if remove:
        _, status = call(api.items.remove, key=key, name=remove)
        assert status == 200
        flash(f"Removed item: {remove}", 'info')

    return redirect(url_for('admin.detail', key=key))
