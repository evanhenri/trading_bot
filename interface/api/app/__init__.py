from flask import Flask

from . import config


def create_app(config_type='development'):
    app_config = {
        'development': config.Development,
        'production' : config.Production,
        'testing'    : config.Testing
    }.get(config_type, config.Development)

    app = Flask(__name__)
    app.config.from_object(app_config)

    from .ui import ui as ui_blueprint
    app.register_blueprint(ui_blueprint)

    from .api import blueprint as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app

