import os

from flask import jsonify, request, session, render_template, send_from_directory
from epi_creator import app
from flask import Flask, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from epi_creator.functions import process_file

print(app.config)


@app.route("/", methods=["GET"])
def hello():
    return render_template("index.html")


@app.route("/download")
def download_file():
    path = request.args.get("filename")  # default_value is optional
    print(path)

    return send_from_directory(
        directory=os.path.dirname(path),
        path=os.path.basename(path),
        as_attachment=True,
    )


@app.route("/upload", methods=["GET", "POST"])
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
                downloadUrl=url_for("download_file", filename=os.path.basename(result))
            )
