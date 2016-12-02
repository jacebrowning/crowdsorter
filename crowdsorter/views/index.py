from flask import (Blueprint, Response,
                   render_template)

# from ._utils import call


blueprint = Blueprint('index', __name__)


@blueprint.route("/")
def get():
    return Response(render_template("index.html"))
