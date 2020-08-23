from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# Instantiate Flask extensions
from pydantic import ValidationError

from app.models.exceptions import InvalidUsage

db = SQLAlchemy()
migrate = Migrate()


def create_app(extra_config_settings=None):
    """Create a Flask application.
    """
    # Instantiate Flask
    if extra_config_settings is None:
        extra_config_settings = {}

    app = Flask(__name__)

    @app.errorhandler(InvalidUsage)
    def app_error_handler(e: InvalidUsage):
        return jsonify({"status": e.msg}), e.code

    @app.errorhandler(ValidationError)
    def app_error_handler(e: ValidationError):
        return jsonify({"errors": e.json()}), 400

    # Load common settings
    app.config.from_object('app.settings')
    # Load environment specific settings
    app.config.from_object('app.local_settings')
    # Load extra settings from extra_config_settings param
    app.config.update(extra_config_settings)

    # Setup Flask-SQLAlchemy
    db.init_app(app)

    # Setup Flask-Migrate
    migrate.init_app(app, db)

    # Register blueprints
    from .endpoints import register_blueprints
    register_blueprints(app)

    return app
