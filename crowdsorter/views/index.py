from flask import Blueprint, Response, render_template
from flask_menu import register_menu


blueprint = Blueprint('index', __name__)


@blueprint.route("/")
@register_menu(blueprint, '.get', "Home", order=0)
def get():
    return Response(render_template("index.html"))
