import logging

from webargs import core
from webargs.flaskparser import FlaskParser
from marshmallow import Schema, fields, pre_load, post_load

from ._exceptions import UnprocessableEntity


parser = FlaskParser(('form', 'data'))
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

    def handle_error(self, exc, data):
        log.error("Unable to parse: %r", data)
        raise UnprocessableEntity(exc.messages)

    class Meta:
        strict = True


class ItemSchema(ValidatorMixin, Schema):

    name = fields.Str(required=True)

    def handle_error(self, error, data):
        log.error("Unable to parse: %r", data)
        raise UnprocessableEntity("Name is required.")
