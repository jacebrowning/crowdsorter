from flask import Blueprint, Response


blueprint = Blueprint('rooms', __name__, url_prefix="/rooms")


@blueprint.route("/")
def index():
    return Response("This is the collections index.")
