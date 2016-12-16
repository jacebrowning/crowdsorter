import logging

from flask_api import FlaskAPI

from . import api
from . import views
from . import extensions


log = logging.getLogger(__name__)


def create_app(config):
    app = FlaskAPI(__name__)
    app.config.from_object(config)

    configure_logging(app)

    register_blueprints(app)
    register_extensions(app)

    return app


def configure_logging(app):
    if app.config['DEBUG']:
        level = logging.DEBUG
        pattern = "%(levelname)s: %(name)s:%(lineno)d: %(message)s"
    else:
        level = logging.INFO
        pattern = "%(levelname)s: %(message)s"
    logging.basicConfig(level=level, format=pattern)


def register_blueprints(app):
    register_backend(app)
    register_frontend(app)


def register_backend(app):
    app.register_blueprint(api.root.blueprint)
    app.register_blueprint(api.collections.blueprint)
    app.register_blueprint(api.votes.blueprint)
    app.register_blueprint(api.scores.blueprint)


def register_frontend(app):
    app.register_blueprint(views.index.blueprint)
    app.register_blueprint(views.collections.blueprint)


def register_extensions(app):
    extensions.db.init_app(app)
    extensions.bootstrap.init_app(app)
    extensions.menu.init_app(app)
