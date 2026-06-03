RESOURCE_DISPLAY_NAMES = {
    "MedicinalProductDefinition": "Medicinal Product",
    "RegulatedAuthorization": "Regulated Auth",
    "ManufacturedItemDefinition": "Manufactured Item",
    "AdministrableProductDefinition": "Administrable Product",
    "PackagedProductDefinition": "Packaged Product",
    "ClinicalUseDefinition": "Clinical Use",
    "Organization": "Organization",
    "Substance": "Substance",
    "Ingredient": "Ingredient",
    "Composition": "Composition",
    "Bundle": "Bundle",
}


def validate_row(row, sheet, session_data=None):
    """Return list of (field_key, message) for a single row.

    field_key is the form column name (e.g. "name", "identifier") so
    templates can attach .field-error to the right input. Use
    "__sheet__" for sheet-level errors that don't map to one input.
    """
    from epi_creator.lookup import get_lookup

    errors = []

    def err(field_key, msg):
        errors.append((field_key, msg))

    def check_spaces(value, field_key, field_label):
        if value and isinstance(value, str) and " " in value:
            err(field_key, f"{field_label} cannot contain spaces")

    def check_numeric(value, field_key, field_label):
        if value and isinstance(value, str) and value.strip():
            try:
                float(value)
            except ValueError:
                err(field_key, f"{field_label} must be a number")
        elif value is None or (isinstance(value, str) and value.strip() == ""):
            pass
        else:
            try:
                float(value)
            except (ValueError, TypeError):
                err(field_key, f"{field_label} must be a number")

    def check_no_newline(value, field_key, field_label):
        if value and isinstance(value, str) and "\n" in value:
            err(field_key, f"{field_label} cannot contain newlines")

    def check_required(value, field_key, field_label):
        if not value or (isinstance(value, str) and value.strip() == ""):
            err(field_key, f"{field_label} is required")

    LABEL_MAP = {"doseForm": "Dose Form", "unit_presentation": "Unit Presentation", "route": "Route of Admin"}

    if sheet == "AdministrableProductDefinition":
        check_required(row.get("identifier"), "identifier", "Identifier")
        check_numeric(row.get("unit_presentationID"), "unit_presentationID", "Unit Presentation ID")
        check_numeric(row.get("routeID"), "routeID", "Route ID")
        check_numeric(row.get("doseFormID"), "doseFormID", "Dose Form ID")
        for fk, lookup_key in (("doseForm", "doseForms"),
                               ("unit_presentation", "unitPresentations"),
                               ("route", "routes")):
            val = (row.get(fk) or "").strip()
            if val and val not in get_lookup(lookup_key):
                label = LABEL_MAP.get(fk, fk)
                err(fk, f"{label} '{val}' is not in the controlled vocabulary. Pick from the list.")

    elif sheet == "Ingredient":
        check_required(row.get("name"), "name", "Name")
        check_required(row.get("role"), "role", "Role")
        check_spaces(row.get("identifier"), "identifier", "Identifier")
        check_spaces(row.get("StrengthBasis"), "StrengthBasis", "Strength Basis")
        check_numeric(row.get("quantity"), "quantity", "Quantity")
        check_no_newline(row.get("name"), "name", "Name")
        role = (row.get("role") or "").lower()
        if role in ("active", "ativo"):
            if not row.get("StrengthBasis") or str(row.get("StrengthBasis")).strip() == "":
                err("StrengthBasis", "Strength Basis is required for active ingredients")
            if not row.get("quantity") or str(row.get("quantity")).strip() == "":
                err("quantity", "Quantity is required for active ingredients")
            if not row.get("identifier") or str(row.get("identifier")).strip() == "":
                err("identifier", "Identifier is required for active ingredients (substance code)")

        ingredient_identifier = (row.get("identifier") or "").strip()
        if ingredient_identifier:
            substance_ids = set()
            if session_data and session_data.get("Substance"):
                for srow in session_data["Substance"]:
                    sid = (srow.get("identifier") or "").strip()
                    if sid:
                        substance_ids.add(sid)
            if not substance_ids:
                err(
                    "identifier",
                    "No Substance defined yet. Please add the substance (with its GSRS identifier) in the Substance step before linking it here.",
                )
            elif ingredient_identifier not in substance_ids:
                err(
                    "identifier",
                    f"Identifier '{ingredient_identifier}' does not match any Substance. "
                    "Add a Substance with this GSRS identifier first, or correct the identifier.",
                )

    elif sheet == "ManufacturedItemDefinition":
        check_required(row.get("identifier"), "identifier", "Identifier")
        check_numeric(row.get("unit_presentationID"), "unit_presentationID", "Unit Presentation ID")
        check_numeric(row.get("doseFormID"), "doseFormID", "Dose Form ID")
        check_spaces(row.get("identifier"), "identifier", "Identifier")
        for fk, lookup_key in (("doseForm", "doseForms"),
                               ("unit_presentation", "unitPresentations")):
            val = (row.get(fk) or "").strip()
            if val and val not in get_lookup(lookup_key):
                label = LABEL_MAP.get(fk, fk)
                err(fk, f"{label} '{val}' is not in the controlled vocabulary. Pick from the list.")

    elif sheet == "MedicinalProductDefinition":
        check_required(row.get("productname"), "productname", "Product Name")
        check_required(row.get("inventedNamePart"), "inventedNamePart", "Invented Name Part")
        check_required(row.get("ScientificNamePart"), "ScientificNamePart", "Scientific Name Part")
        check_required(row.get("StrengthPart"), "StrengthPart", "Strength Part")
        check_required(row.get("PharmaceuticalDosePart"), "PharmaceuticalDosePart", "Pharmaceutical Dose Part")
        check_required(row.get("country"), "country", "Country")
        check_required(row.get("countryCode"), "countryCode", "Country Code")
        check_required(row.get("language"), "language", "Language")
        check_required(row.get("languageID"), "languageID", "Language ID")
        check_required(row.get("statusSuply"), "statusSuply", "Status Supply")
        check_spaces(row.get("countryCode"), "countryCode", "Country Code")
        check_numeric(row.get("statusSuplyID"), "statusSuplyID", "Status Supply ID")
        check_no_newline(row.get("productname"), "productname", "Product Name")
        check_no_newline(row.get("inventedNamePart"), "inventedNamePart", "Invented Name Part")
        check_no_newline(row.get("ScientificNamePart"), "ScientificNamePart", "Scientific Name Part")
        check_no_newline(row.get("StrengthPart"), "StrengthPart", "Strength Part")
        check_no_newline(row.get("PharmaceuticalDosePart"), "PharmaceuticalDosePart", "Pharmaceutical Dose Part")

    elif sheet == "Organization":
        check_required(row.get("name"), "name", "Name")
        check_required(row.get("type"), "type", "Organization Type")
        check_required(row.get("identifier"), "identifier", "Identifier")
        check_required(row.get("address_line"), "address_line", "Address Line")
        check_required(row.get("address_city"), "address_city", "City")
        check_required(row.get("address_country"), "address_country", "Country")
        check_spaces(row.get("identifier"), "identifier", "Identifier")
        check_numeric(row.get("address_postalCode"), "address_postalCode", "Postal Code")
        check_numeric(row.get("typeID"), "typeID", "Type ID")
        check_no_newline(row.get("name"), "name", "Name")

    elif sheet == "PackagedProductDefinition":
        check_required(row.get("name"), "name", "Name")
        check_required(row.get("statusDate"), "statusDate", "Status Date")
        check_required(row.get("packaging_quantity"), "packaging_quantity", "Pkg Qty")
        check_required(row.get("packaging_identifier"), "packaging_identifier", "Pkg ID")
        check_spaces(row.get("identifier"), "identifier", "Identifier")
        check_numeric(row.get("packaging_quantity"), "packaging_quantity", "Pkg Qty")
        check_no_newline(row.get("name"), "name", "Name")

    elif sheet == "Substance":
        check_required(row.get("name"), "name", "Name")
        check_required(row.get("identifier"), "identifier", "Identifier")
        check_no_newline(row.get("name"), "name", "Name")
        check_spaces(row.get("identifier"), "identifier", "Identifier")

    elif sheet == "ClinicalUseDefinition":
        check_required(row.get("type"), "type", "Type")
        check_required(row.get("name"), "name", "Name")
        check_required(row.get("conceptID"), "conceptID", "Concept ID")
        check_required(row.get("concept"), "concept", "Concept")
        check_no_newline(row.get("name"), "name", "Name")
        check_spaces(row.get("identifier"), "identifier", "Identifier")
        check_numeric(row.get("conceptID"), "conceptID", "Concept ID")
        if row.get("type") and row.get("type") not in ("Indication", "Contraindication", "Interaction"):
            err("type", "Type must be one of: Indication, Contraindication, Interaction")

    elif sheet == "Composition":
        check_required(row.get("language"), "language", "Language")
        check_required(row.get("date"), "date", "Date")
        check_required(row.get("name"), "name", "Name")
        check_required(row.get("identifier_system"), "identifier_system", "Identifier System")
        check_no_newline(row.get("name"), "name", "Name")

    elif sheet == "RegulatedAuthorization":
        check_required(row.get("identifier"), "identifier", "Identifier")
        check_required(row.get("statusDate"), "statusDate", "Status Date")
        check_required(row.get("reference"), "reference", "Reference")
        check_spaces(row.get("identifier"), "identifier", "Identifier")
        if row.get("reference") and row.get("reference") not in ("MedicinalProduct", "PackagedProduct"):
            err("reference", "Reference must be MedicinalProduct or PackagedProduct")
        if row.get("regionID") and str(row.get("regionID")).strip() != "":
            check_numeric(row.get("regionID"), "regionID", "Region ID")

    elif sheet == "Bundle":
        check_required(row.get("language"), "language", "Language")
        check_required(row.get("identifier_system"), "identifier_system", "Identifier System")
        check_required(row.get("identifier_value"), "identifier_value", "Identifier Value")

    return errors


STEP_TO_SHEET = {
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


def is_step_complete(step_key, session_data):
    """Return (is_complete, blockers) for a given wizard step.

    A step is complete when it has at least one row that passes
    per-row validation. Cross-sheet constraints (e.g. Substance for
    Ingredient) are evaluated through validate_row.
    """
    sheet = STEP_TO_SHEET.get(step_key)
    if sheet is None:
        return False, [f"Unknown step: {step_key}"]
    rows = (session_data or {}).get(sheet, [])
    if not rows:
        display = RESOURCE_DISPLAY_NAMES.get(sheet, sheet)
        return False, [f"{display} has no entries yet."]
    blockers = []
    for i, row in enumerate(rows):
        for _fk, msg in validate_row(row, sheet, session_data=session_data):
            blockers.append(f"Row {i + 1}: {msg}")
    return (len(blockers) == 0), blockers


MULTI_ROW_SHEETS = {
    "Organization",
    "Substance",
    "Ingredient",
    "RegulatedAuthorization",
    "ClinicalUseDefinition",
    "Composition",
    "PackagedProductDefinition",
}

HTML_FIELDS = {
    "package_leaflet",
    "information_user",
    "what_in_leaflet",
    "what_product_is",
    "before_take",
    "how_to_take",
    "side_effects",
    "how_to_store",
    "other_info",
}

ALLOWED_HTML_TAGS = {
    "p", "br", "h1", "h2", "h3", "h4", "h5", "h6",
    "ul", "ol", "li", "b", "i", "em", "strong",
    "div", "span", "a", "table", "tr", "td", "th", "thead", "tbody",
}
ALLOWED_HTML_ATTRS = {"a": {"href", "title"}}


def sanitize_html(value):
    """Strip dangerous tags/attrs from a user-supplied HTML fragment.

    Used for the Composition step's package_leaflet and similar
    fields, which are intentionally HTML but must not allow
    <script>, on* handlers, javascript: URLs, etc.
    """
    if not value:
        return value
    import nh3
    return nh3.clean(
        str(value),
        tags=ALLOWED_HTML_TAGS,
        attributes=ALLOWED_HTML_ATTRS,
        url_schemes={"https", "mailto"},
    )


def validate_sheet_data(rows, sheet_name, session_data=None):
    """Return [(row_idx, [(field_key, msg), ...]), ...] for each row with errors.

    Sheets that allow multiple rows (e.g. Substance, Ingredient) require
    at least one entry. A sheet-level error with field_key='__sheet__'
    is returned in that case so it shows up in the form-errors banner.
    """
    all_errors = []
    if sheet_name in MULTI_ROW_SHEETS and not rows:
        display = RESOURCE_DISPLAY_NAMES.get(sheet_name, sheet_name)
        all_errors.append((0, [("__sheet__", f"At least one {display} entry is required.")]))
        return all_errors
    for idx, row in enumerate(rows):
        errs = validate_row(row, sheet_name, session_data=session_data)
        if errs:
            all_errors.append((idx, errs))
    return all_errors


def validate_pre_generation(session_data):
    errors = []

    required_sheets = [
        "MedicinalProductDefinition",
        "Organization",
        "Ingredient",
        "AdministrableProductDefinition",
        "ManufacturedItemDefinition",
        "Bundle",
    ]
    for sheet in required_sheets:
        if not session_data.get(sheet) or len(session_data[sheet]) == 0:
            display = RESOURCE_DISPLAY_NAMES.get(sheet, sheet)
            errors.append(f"{display} is required. Please fill in the form.")

    singles = [
        "MedicinalProductDefinition",
        "ManufacturedItemDefinition",
        "AdministrableProductDefinition",
    ]
    for sheet in singles:
        if sheet in session_data and len(session_data[sheet]) > 1:
            display = RESOURCE_DISPLAY_NAMES.get(sheet, sheet)
            errors.append(
                f"{display} must have exactly one entry. Found {len(session_data[sheet])}."
            )

    if "Ingredient" in session_data:
        has_active = any(
            (r.get("role") or "").lower() in ("active", "ativo")
            for r in session_data["Ingredient"]
        )
        if not has_active:
            errors.append("At least one active ingredient is required.")

        substance_ids = {
            (s.get("identifier") or "").strip()
            for s in session_data.get("Substance", [])
            if (s.get("identifier") or "").strip()
        }
        for idx, ing in enumerate(session_data["Ingredient"]):
            ing_id = (ing.get("identifier") or "").strip()
            if not ing_id:
                continue
            if ing_id not in substance_ids:
                errors.append(
                    f"Ingredient #{idx + 1} ('{ing.get('name', '')}') references substance "
                    f"identifier '{ing_id}' which is not defined in the Substance step."
                )

    orgs = session_data.get("Organization", [])
    has_mah = any(
        (r.get("type") or "").lower() == "marketing authorisation holder"
        for r in orgs
    )
    if not has_mah:
        errors.append("At least one Marketing Authorisation Holder organization is required.")

    return errors
