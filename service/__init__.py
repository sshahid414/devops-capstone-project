"""
Package: service

Package for the application models and service routes.
This module creates and configures the Flask app and sets up logging,
the SQL database, and the Talisman / CORS security layers.
"""
import sys
from flask import Flask
from flask_talisman import Talisman
from flask_cors import CORS
from service import config
from service.common import log_handlers

# Create the Flask application
app = Flask(__name__)
app.config.from_object(config)

# Add security headers with Flask-Talisman and enable CORS policies.
# force_https is turned off so the service works behind the lab proxy and
# during local/unit testing. Tests toggle talisman.force_https as needed.
talisman = Talisman(
    app,
    force_https=False,
    content_security_policy={
        "default-src": "'self'",
        "object-src": "'none'",
    },
    referrer_policy="strict-origin-when-cross-origin",
)
CORS(app)

# Import the routes AFTER the Flask app object is created
from service import routes, models  # noqa: F401 E402 pylint: disable=wrong-import-position
from service.common import error_handlers, cli_commands  # noqa: F401 E402 pylint: disable=wrong-import-position

# Set up logging for production
log_handlers.init_logging(app, "gunicorn.error")

app.logger.info(70 * "*")
app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info(70 * "*")

try:
    models.init_db(app)  # make our database tables
except Exception as error:  # pylint: disable=broad-except
    app.logger.critical("%s: Cannot continue", error)
    # gunicorn requires exit code 4 to stop spawning workers when they die
    sys.exit(4)

app.logger.info("Service initialized!")
