import os

from flask import (
    Blueprint,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from flask import current_app as app

from epi_creator.functions import generate_from_session
from epi_creator.validator import (
    is_step_complete,
    validate_sheet_data,
    validate_pre_generation,
)
from epi_creator.lookup import get_lookup, get_category_id

gh_epi_creator = Blueprint("gh_epi_creator", __name__)

STEPS = [
    "organization",
    "medicinal-product",
    "substance",
    "ingredient",
    "regulated-auth",
    "manufactured-item",
    "administrable-product",
    "packaged-product",
    "clinical-use",
    "composition",
    "bundle",
]

SHEET_NAMES = {
    "organization": "Organization",
    "medicinal-product": "MedicinalProductDefinition",
    "substance": "Substance",
    "ingredient": "Ingredient",
    "regulated-auth": "RegulatedAuthorization",
    "manufactured-item": "ManufacturedItemDefinition",
    "administrable-product": "AdministrableProductDefinition",
    "packaged-product": "PackagedProductDefinition",
    "clinical-use": "ClinicalUseDefinition",
    "composition": "Composition",
    "bundle": "Bundle",
}


@gh_epi_creator.before_request
def log_request_info():
    app.logger.info(f"Request: {request.method} {request.path}")


@gh_epi_creator.route("/", methods=["GET"])
def hello():
    return render_template("index.html")


@gh_epi_creator.route("/faq", methods=["GET"])
def faq():
    return render_template("faq.html")


@gh_epi_creator.route("/wizard/new", methods=["POST"])
def wizard_new():
    session.clear()
    session["data"] = {}
    return redirect(url_for("gh_epi_creator.wizard_step", step=STEPS[0]))


@gh_epi_creator.route("/wizard/<step>", methods=["GET"])
def wizard_step(step):
    if "data" not in session:
        session["data"] = {}
    data = session["data"]
    sheet_name = SHEET_NAMES.get(step)

    if step in STEPS and step != STEPS[0]:
        target_idx = STEPS.index(step)
        for prior in STEPS[:target_idx]:
            ok, _ = is_step_complete(prior, data)
            if not ok:
                return redirect(url_for("gh_epi_creator.wizard_step", step=prior))

    rows = data.get(sheet_name, [])
    is_single = sheet_name in (
        "MedicinalProductDefinition",
        "ManufacturedItemDefinition",
        "AdministrableProductDefinition",
    )

    step_template = step.replace("-", "_") + ".html"
    ctx = dict(step=step, sheet_name=sheet_name, rows=rows, steps=STEPS,
               current_step=step, step_title=sheet_name.replace("Definition", ""),
               is_single=is_single, base_template="wizard/base.html",
               languages=get_lookup("languages"),
               step_states=_step_states(data))
    if request.headers.get("HX-Request"):
        return _render_htmx(step_template, **ctx)
    return render_template("wizard/" + step_template, **ctx)


@gh_epi_creator.route("/wizard/<step>", methods=["POST"])
def wizard_submit(step):
    if "data" not in session:
        session["data"] = {}
    sheet_name = SHEET_NAMES.get(step)

    form_data = request.form.to_dict(flat=False)

    if sheet_name == "Substance":
        form_data = _consolidate_substance_mw(form_data)

    rows = _parse_form_rows(form_data, sheet_name)

    validation_errors = validate_sheet_data(rows, sheet_name, session_data=session.get("data"))

    is_single = sheet_name in (
        "MedicinalProductDefinition",
        "ManufacturedItemDefinition",
        "AdministrableProductDefinition",
    )

    step_template = step.replace("-", "_") + ".html"
    ctx = dict(step=step, sheet_name=sheet_name, rows=rows, steps=STEPS,
               current_step=step, step_title=sheet_name.replace("Definition", ""),
               is_single=is_single, base_template="wizard/base.html",
               languages=get_lookup("languages"),
               step_states=_step_states(session.get("data", {})))

    if validation_errors:
        if request.headers.get("HX-Request"):
            return _render_htmx(step_template, errors=validation_errors, **ctx)
        ctx["errors"] = validation_errors
        return render_template("wizard/" + step_template, **ctx)

    rows = _consolidate_pipe_fields(rows, sheet_name)
    session["data"][sheet_name] = rows
    session.modified = True

    current_idx = STEPS.index(step)
    if current_idx < len(STEPS) - 1:
        next_step = STEPS[current_idx + 1]
    else:
        next_step = "bundle"

    redirect_url = url_for("gh_epi_creator.wizard_step", step=next_step)

    if request.headers.get("HX-Request"):
        resp = make_response("")
        resp.headers["HX-Redirect"] = redirect_url
        return resp

    return redirect(redirect_url)


@gh_epi_creator.route("/wizard/generate", methods=["POST"])
def wizard_generate():
    if "data" not in session or not session["data"]:
        return "<div class='alert alert-danger'>No data to generate. Please fill in the forms first.</div>"

    pre_gen_errors = validate_pre_generation(session["data"])
    if pre_gen_errors:
        items = "".join(f"<li>{e}</li>" for e in pre_gen_errors)
        return f"<div class='alert alert-danger'><ul>{items}</ul></div>"

    productname = "epi-product"
    mp = session["data"].get("MedicinalProductDefinition", [{}])
    if mp and mp[0].get("productname"):
        productname = mp[0]["productname"].replace(" ", "_")

    try:
        zip_path = generate_from_session(session["data"], productname)
        download_url = url_for(
            "gh_epi_creator.wizard_download", filename=os.path.basename(zip_path)
        )
        return f"<div class='generated-link'><a href='{download_url}' class='btn btn-primary' download>Download Results (ZIP)</a></div>"
    except Exception as e:
        return f"<div class='alert alert-danger'>Generation failed: {str(e)}</div>"


@gh_epi_creator.route("/wizard/download")
def wizard_download():
    filename = request.args.get("filename", "")
    directory = os.path.dirname(filename)
    if not directory:
        directory = "."
    return send_from_directory(
        directory=directory,
        path=os.path.basename(filename),
        as_attachment=True,
    )


@gh_epi_creator.route("/api/lookup/<category>", methods=["GET"])
def api_lookup(category):
    q = request.args.get("q", "").lower()
    items = get_lookup(category)

    if q:
        items = [i for i in items if q in str(i).lower()]

    category_to_id = {
        "doseForms": "doseForm",
        "routes": "route",
        "unitPresentations": "unitPresentation",
    }

    result = []
    for item in items[:50]:
        if isinstance(item, dict):
            result.append(item)
        else:
            entry = {"label": str(item), "value": str(item)}
            id_category = category_to_id.get(category)
            if id_category:
                code = get_category_id(id_category, str(item))
                if code:
                    entry["id"] = code
            result.append(entry)
    return jsonify(result)


def _parse_form_rows(form_data, sheet_name):
    rows = []

    row_counts = []
    for k, v in form_data.items():
        if k.startswith("row_count"):
            try:
                row_counts.append(int(v[0]))
            except (ValueError, TypeError):
                pass

    max_rows = max(row_counts) if row_counts else 1

    for i in range(max_rows):
        row = {}
        suffix = "_" + str(i)
        for key, values in form_data.items():
            if key.startswith("row_count"):
                continue
            if key.endswith(suffix):
                col_name = key[: -len(suffix)]
                row[col_name] = values[0] if values else ""
        if row and any(
            str(v).strip() for k, v in row.items() if k != "id"
        ):
            rows.append(row)

    if not rows and max_rows == 1:
        row = {}
        for key, values in form_data.items():
            if key.startswith("row_count"):
                continue
            row[key] = values[0] if values else ""
        if row and any(
            str(v).strip() for k, v in row.items() if k != "id"
        ):
            rows.append(row)

    return rows


def _consolidate_pipe_fields(rows, sheet_name):
    if sheet_name == "MedicinalProductDefinition":
        for row in rows:
            id_systems = []
            id_values = []
            cls_ids = []
            cls_texts = []
            for k, v in sorted(row.items()):
                if k.startswith("identifier_system_0_p"):
                    id_systems.append(v)
                elif k.startswith("identifier_value_0_p"):
                    id_values.append(v)
                elif k.startswith("classification_ids_0_p"):
                    cls_ids.append(v)
                elif k.startswith("classification_texts_0_p"):
                    cls_texts.append(v)
            if id_systems or id_values:
                row["identifier_system"] = "|".join(filter(None, id_systems))
                row["identifier_value"] = "|".join(filter(None, id_values))
            if cls_ids or cls_texts:
                row["classification_ids"] = "|".join(filter(None, cls_ids))
                row["classification_texts"] = "|".join(filter(None, cls_texts))
            for k in list(row.keys()):
                if "_0_p" in k:
                    del row[k]
    return rows


def _consolidate_substance_mw(form_data):
    mw_counts = {}
    for k in list(form_data.keys()):
        if k.startswith("mw_count_"):
            try:
                idx = int(k.split("_")[2])
                mw_counts[idx] = int(form_data[k][0])
            except (IndexError, ValueError):
                pass

    for substance_idx, count in mw_counts.items():
        values = []
        types = []
        for mw_idx in range(count):
            v_key = f"mw_value_{substance_idx}_{mw_idx}"
            t_key = f"mw_type_{substance_idx}_{mw_idx}"
            if v_key in form_data:
                values.append(form_data[v_key][0])
            if t_key in form_data:
                types.append(form_data[t_key][0])
        form_data[f"moleclularWeigth_{substance_idx}"] = ["|".join(values)]
        form_data[f"moleclularWeigthType_{substance_idx}"] = ["|".join(types)]

    for k in list(form_data.keys()):
        if k.startswith("mw_value_") or k.startswith("mw_type_") or k.startswith("mw_count_"):
            del form_data[k]

    return form_data


def _render_htmx(template_name, **context):
    context["base_template"] = "wizard/_htmx_base.html"
    return render_template("wizard/" + template_name, **context)


def _step_states(session_data):
    return {s: is_step_complete(s, session_data)[0] for s in STEPS}


# ---- keep download endpoint for backward compat / template download ----
@gh_epi_creator.route("/download")
def download_file():
    path = request.args.get("filename", "")
    if not path:
        return "No filename", 400
    return send_from_directory(
        directory=os.path.dirname(path) if os.path.dirname(path) else ".",
        path=os.path.basename(path),
        as_attachment=True,
    )
