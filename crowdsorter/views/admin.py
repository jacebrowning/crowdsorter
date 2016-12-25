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
    content, status = call(api.scores.index, key=key)
    if status == 404:
        content['name'] = UNKNOWN_COLLECTION_NAME

    return Response(render_template("admin.html", collection=content))


@blueprint.route("/collections/<key>", methods=['POST'])
def update(key):
    # TODO: process update
    # name = request.form['name'].strip()

    # _, status = call(api.collections.update, key=key)
    # assert status == 200

    return redirect(url_for('admin.detail', key=key))
