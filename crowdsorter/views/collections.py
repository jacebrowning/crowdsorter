from flask import Blueprint, Response


blueprint = Blueprint('collections', __name__)


@blueprint.route("/collections/")
def index():
    return Response("This is the collections index.")
