import logging

from flask import Blueprint, Response
from flask import (request, render_template, redirect, url_for, flash,
                   current_app)
from flask_menu import register_menu

from .. import api

from ._utils import call, parts, send_email


UNKNOWN_COLLECTION_NAME = "No Such Collection"
UNKNOWN_COLLECTION_CODE = "unknown"

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
        content['code'] = UNKNOWN_COLLECTION_CODE
        content['items'] = []

    return Response(render_template("admin.html", collection=content))


@blueprint.route("/collections/<key>", methods=['POST'])
def update(key):
    email = request.form.get('email', "").strip()
    name = request.form.get('name', "").strip()
    code = request.form.get('code', "").strip()
    private = not request.form.getlist('public')
    locked = not request.form.getlist('unlocked')
    save = request.form.get('save')
    add = request.form.get('add', '').strip()
    remove = request.form.get('remove', '').strip()
    view = request.form.get('view')
    clear = request.form.get('clear')
    delete = request.form.get('delete')
    log.debug(f"Values: email={email} name={name} code={code}")
    log.debug(f"Options: private={private} locked={locked}")
    log.debug(f"Actions: save={save} add={add} remove={remove} view={view} "
              f"clear={clear} delete={delete}")

    if email:
        content, status = call(api.collections.update, key=key, owner=email)
        if status == 200:

            name = content['name']
            url = url_for('admin.detail', key=content['key'], _external=True)

            if send_email(
                subject=f"Crowd Sorter: {name}",
                to_email=content['owner'],
                text=f"The admin page for {name} can be found at: {url}",
            ):
                flash(f"Email sent: {email}", 'info')

            else:
                flash(f"Unable to send email: {email}", 'danger')

        else:
            flash(content['message'], 'danger')

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

    if view:
        content, status = call(api.collections.detail, key=key)
        assert status == 200
        code = content['code']
        return redirect(url_for('collections.detail', code=code))

    if clear:
        content, status = call(api.votes.clear, key=key)
        assert status == 200
        flash("Votes cleared.", 'info')
        code = content['code']
        return redirect(url_for('collections.detail', code=code))

    if delete:
        _, status = call(api.collections.delete, key=key)
        assert 200 <= status < 300
        return redirect(url_for('collections.index'))

    return redirect(url_for('admin.detail', key=key))
