# server/config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))

def set_flask_config(app):
    """Flask configuration."""
    app.config["SECRET_KEY"] = os.getenv('FLASK_SECRET_KEY', "flask_secret_key")
    app.config["DEBUG"] = False