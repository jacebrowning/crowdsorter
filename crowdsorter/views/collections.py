import logging

from flask import Blueprint
from flask import (request, current_app,
                   render_template, redirect, url_for, flash)
from flask_menu import register_menu

from .. import api

from ._navbar import activate_collections
from ._utils import call


blueprint = Blueprint('collections', __name__)
log = logging.getLogger(__name__)


@blueprint.route("/collections/")
@register_menu(blueprint, '.index', "Collections", order=1,
               active_when=activate_collections)
def index():
    query = request.args.get('q')

    content, status = call(api.collections.index, query=query, private=False,
                           limit=13, token=current_app.config['AUTH_TOKEN'])

    assert status == 200

    return render_template("collections.html", collections=content['_objects'])


@blueprint.route("/collections/", methods=['POST'])
def new():
    name = request.form.get('name', "").strip()

    if not name:
        flash("A name is required.", 'danger')
        return redirect(url_for('collections.index'))

    content, status = call(api.collections.create, name=name)
    assert status == 201

    flash("Welcome to your new collection!", 'info')

    return redirect(url_for('admin.detail', key=content['key']))
