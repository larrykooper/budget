import os
from logging.config import dictConfig

from flask import Flask
from flask import render_template

from src.flask_app.ingesting import ingest_blueprint
from src.flask_app.reporting import report_blueprint
from src.flask_app.rules import rules_blueprint


def create_app(test_config=None):
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
})

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='q.3-bNRts7V4JUKKLDQxvB*AaxeKVnobXy-MnRKksHnWsnPZi!',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Home Page
    @app.route('/')
    def homepage():
        return render_template('homepage/homepage.html')

    # Register blueprints

    app.register_blueprint(report_blueprint.bp)
    app.register_blueprint(ingest_blueprint.bp)
    app.register_blueprint(rules_blueprint.bp)

    return app
