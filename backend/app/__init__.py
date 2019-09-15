# -*- coding: utf-8 -*-
#
from flask import Flask, render_template

from app.extensions import cors, db, migrate
from app.api_v1 import api_bp_v1


def initialize_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)

    if app.config["ENV"] == "development":
        cors.init_app(app)


def register_blueprints(app):
    app.register_blueprint(api_bp_v1, url_prefix="/api/v1")


def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    initialize_extensions(app)
    register_blueprints(app)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
