import os

from flask import (
    Blueprint,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask import current_app as app
from werkzeug.utils import secure_filename

from epi_creator.functions import process_file

gh_epi_creator = Blueprint("gh_epi_creator", __name__)


@gh_epi_creator.before_request
def log_request_info():
    app.logger.info(f"Request: {request.method} {request.path}")


@gh_epi_creator.route("/", methods=["GET"])
def hello():
    return render_template("index.html")


@gh_epi_creator.route("/faq", methods=["GET"])
def faq():
    return render_template("faq.html")


@gh_epi_creator.route("/download")
def download_file():
    path = request.args.get("filename")  # default_value is optional
    print(path)

    return send_from_directory(
        directory=os.path.dirname(path),
        path=os.path.basename(path),
        as_attachment=True,
    )


@gh_epi_creator.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # if user does not select file, browser also submits an empty part without filename
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            result = process_file(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            print(result)
            return jsonify(
                downloadUrl=url_for(
                    "gh_epi_creator.download_file", filename=os.path.basename(result)
                )
            )
