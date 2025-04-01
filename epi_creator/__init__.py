"""Flask app for starting server."""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from flask import Flask


class StreamToLogger:
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level

    def write(self, message):
        message = message.strip()
        if message:
            self.logger.log(self.level, message)

    def flush(self):
        pass


def create_app():
    app = Flask(__name__)

    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )
    # Main app log
    app_log_file = os.path.join(log_dir, "app.log")
    app_handler = RotatingFileHandler(
        app_log_file, maxBytes=10 * 1024 * 1024, backupCount=10
    )
    app_handler.setLevel(logging.INFO)
    app_handler.setFormatter(formatter)
    app.logger.addHandler(app_handler)
    app.logger.setLevel(logging.INFO)

    # stdout log
    stdout_log_file = os.path.join(log_dir, "stdout.log")
    stdout_handler = RotatingFileHandler(
        stdout_log_file, maxBytes=10 * 1024 * 1024, backupCount=10
    )
    stdout_handler.setLevel(logging.INFO)
    stdout_handler.setFormatter(formatter)
    stdout_logger = logging.getLogger("stdout_logger")
    stdout_logger.setLevel(logging.INFO)
    stdout_logger.addHandler(stdout_handler)

    # stderr log
    stderr_log_file = os.path.join(log_dir, "stderr.log")
    stderr_handler = RotatingFileHandler(
        stderr_log_file, maxBytes=10 * 1024 * 1024, backupCount=10
    )
    stderr_handler.setLevel(logging.ERROR)
    stderr_handler.setFormatter(formatter)
    stderr_logger = logging.getLogger("stderr_logger")
    stderr_logger.setLevel(logging.ERROR)
    stderr_logger.addHandler(stderr_handler)

    # Redirect print() and uncaught exceptions
    sys.stdout = StreamToLogger(stdout_logger, logging.INFO)
    sys.stderr = StreamToLogger(stderr_logger, logging.ERROR)
    # Example log
    app.logger.info("Starting GH EPI Creator app")

    from .views import gh_epi_creator

    app.register_blueprint(gh_epi_creator, url_prefix="/gh-epi-creator")
    app.config["UPLOAD_FOLDER"] = "./"
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB limit

    return app
