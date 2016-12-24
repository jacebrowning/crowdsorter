from flask import (Blueprint, Response,
                   current_app, render_template)
from flask_menu import register_menu


blueprint = Blueprint('index', __name__)


@blueprint.route("/")
@register_menu(blueprint, '.get', "Home", order=0)
def get():
    sample = current_app.config['SAMPLE_COLLECTION_CODE']
    return Response(render_template("index.html", sample=sample))
