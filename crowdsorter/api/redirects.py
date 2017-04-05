import logging

from flask import Blueprint, url_for, current_app
from flask_api import status

from ..models import Redirect

from ._schemas import parser, TokenSchema, \
    CreateRedirectSchema, RedirectSchema as UpdateRedirectSchema
from ._serializers import serialize_redirect as serialize
from . import _exceptions as exceptions


blueprint = Blueprint('redirects_api', __name__)
log = logging.getLogger(__name__)


@blueprint.route("/api/redirects/")
@parser.use_kwargs(TokenSchema)
def index(token):
    if token != current_app.config['AUTH_TOKEN']:
        raise exceptions.PermissionDenied

    redirects = Redirect.objects().order_by('start_slug')

    content = dict(
        _links=dict(
            root=url_for('root_api.index', _external=True),
            self=url_for('redirects_api.index', _external=True),
        ),
        _objects=[serialize(r) for r in redirects],
    )

    return content, status.HTTP_200_OK


@blueprint.route("/api/redirects/", methods=['POST'])
@parser.use_kwargs(CreateRedirectSchema)
def create(start_slug, end_slug):
    redirect = Redirect(start_slug=start_slug, end_slug=end_slug)
    redirect.save()

    return serialize(redirect), status.HTTP_201_CREATED


@blueprint.route("/api/redirects/<start_slug>")
def detail(start_slug):
    redirect = Redirect.objects(start_slug=start_slug).first()
    if not redirect:
        raise exceptions.NotFound

    return serialize(redirect), status.HTTP_200_OK


@blueprint.route("/api/redirects/<start_slug>", methods=['PUT'])
@parser.use_kwargs(UpdateRedirectSchema)
def update(start_slug, end_slug):
    redirect = Redirect.objects(start_slug=start_slug).first()
    if not redirect:
        raise exceptions.NotFound

    log.debug("Updating redirect %r => %r", start_slug, end_slug)
    redirect.end_slug = end_slug
    redirect.save()

    return serialize(redirect), status.HTTP_200_OK
