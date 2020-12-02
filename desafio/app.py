# -*- coding: utf-8 -*-
from desafio import settings, commands, currency
from flask import Flask
from desafio.extensions import cache, fpika


def create_app(config_object=settings.ProdConfig):
    app = Flask(__name__.split('.')[0], instance_relative_config=True)
    app.url_map.strict_slashes = False
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_shellcontext(app)
    register_commands(app)
    return app


def register_blueprints(app):
    app.register_blueprint(currency.views.bp)
    app.register_blueprint(currency.views.currencies)


def register_shellcontext(app):
    def shell_context():
        return {
        }
    app.shell_context_processor(shell_context)


def register_extensions(app):
    cache.init_app(app)
    fpika.init_app(app)


def register_commands(app):
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.init_workers)
