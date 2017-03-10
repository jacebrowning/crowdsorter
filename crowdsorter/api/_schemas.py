import logging

from webargs import core
from webargs.flaskparser import FlaskParser
from marshmallow import Schema, fields, pre_load, post_load

from ._exceptions import UnprocessableEntity


parser = FlaskParser(('query', 'form', 'data'))
log = logging.getLogger(__name__)


@parser.location_handler('data')
def parse_data(request, name, field):
    return core.get_value(request.data, name, field)


class ValidatorMixin(object):

    @pre_load
    def log_input(self, data):  # pylint: disable=no-self-use
        log.debug("Input data: %r", data)

    @post_load
    def log_parsed(self, data):  # pylint: disable=no-self-use
        log.debug("Parsed data: %r", data)

    def handle_error(self, error, data):  # pylint: disable=no-self-use
        log.error("Unable to parse: %r", data)

        missing = []
        for field in sorted(error.messages):
            for message in error.messages[field]:
                if message == "Missing data for required field.":
                    missing.append(field)

        if len(missing) == 1:
            msg = f"{missing[0]} is required.".capitalize()
            raise UnprocessableEntity(msg)

        elif len(missing) == 2:
            msg = f"{missing[0]} and {missing[1]} are required.".capitalize()
            raise UnprocessableEntity(msg)

        else:
            raise UnprocessableEntity(error.messages)

    class Meta:
        strict = True


class TokenSchema(ValidatorMixin, Schema):

    token = fields.Str(missing=None)


class CollectionSchema(ValidatorMixin, Schema):

    code = fields.Str(missing=None)


class NewCollectionSchema(CollectionSchema):

    name = fields.Str(required=True)
    items = fields.List(fields.Str(), missing=None)


class EditCollectionSchema(CollectionSchema):

    name = fields.Str(missing=None)
    owner = fields.Str(missing=None)
    private = fields.Bool(missing=None)
    locked = fields.Bool(missing=None)

    @pre_load
    def clean(self, data):  # pylint: disable=no-self-use
        name = data.get('name')
        if name:
            data['name'] = name.strip()

        code = data.get('code')
        if code:
            data['code'] = code.strip().lower().replace(' ', '-')


class ItemSchema(ValidatorMixin, Schema):

    name = fields.Str(required=True)
    description = fields.Str(missing=None)
    image_url = fields.Str(missing=None)
    ref_url = fields.Str(missing=None)


class EditItemSchema(ItemSchema):

    name = fields.Str(missing=None)


class VoteSchema(ValidatorMixin, Schema):

    winner = fields.Str(required=True)
    loser = fields.Str(required=True)
