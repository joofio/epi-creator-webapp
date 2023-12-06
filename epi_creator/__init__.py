"""Flask app for starting server."""
import os
from flask import Flask

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "./"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB limit


import epi_creator.views
