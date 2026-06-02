def validate_row(row, sheet, session_data=None):
    errors = []

    def check_spaces(value, field_label):
        if value and isinstance(value, str) and " " in value:
            errors.append(f"{field_label} cannot contain spaces")

    def check_numeric(value, field_label):
        if value and isinstance(value, str) and value.strip():
            try:
                float(value)
            except ValueError:
                errors.append(f"{field_label} must be a number")
        elif value is None or (isinstance(value, str) and value.strip() == ""):
            pass
        else:
            try:
                float(value)
            except (ValueError, TypeError):
                errors.append(f"{field_label} must be a number")

    def check_no_newline(value, field_label):
        if value and isinstance(value, str) and "\n" in value:
            errors.append(f"{field_label} cannot contain newlines")

    def check_required(value, field_label):
        if not value or (isinstance(value, str) and value.strip() == ""):
            errors.append(f"{field_label} is required")

    if sheet == "AdministrableProductDefinition":
        check_required(row.get("identifier"), "Identifier")
        check_numeric(row.get("unit_presentationID"), "Unit Presentation ID")
        check_numeric(row.get("routeID"), "Route ID")
        check_numeric(row.get("doseFormID"), "Dose Form ID")

    elif sheet == "Ingredient":
        check_required(row.get("name"), "Name")
        check_required(row.get("role"), "Role")
        check_spaces(row.get("identifier"), "Identifier")
        check_spaces(row.get("StrengthBasis"), "Strength Basis")
        check_numeric(row.get("quantity"), "Quantity")
        check_no_newline(row.get("name"), "Name")
        role = (row.get("role") or "").lower()
        if role in ("active", "ativo"):
            if not row.get("StrengthBasis") or str(row.get("StrengthBasis")).strip() == "":
                errors.append("Strength Basis is required for active ingredients")
            if not row.get("quantity") or str(row.get("quantity")).strip() == "":
                errors.append("Quantity is required for active ingredients")
            if not row.get("identifier") or str(row.get("identifier")).strip() == "":
                errors.append("Identifier is required for active ingredients (substance code)")

        ingredient_identifier = (row.get("identifier") or "").strip()
        if ingredient_identifier:
            substance_ids = set()
            if session_data and session_data.get("Substance"):
                for srow in session_data["Substance"]:
                    sid = (srow.get("identifier") or "").strip()
                    if sid:
                        substance_ids.add(sid)
            if not substance_ids:
                errors.append(
                    "No Substance defined yet. Please add the substance (with its GSRS identifier) in the Substance step before linking it here."
                )
            elif ingredient_identifier not in substance_ids:
                errors.append(
                    f"Identifier '{ingredient_identifier}' does not match any Substance. "
                    f"Add a Substance with this GSRS identifier first, or correct the identifier."
                )

    elif sheet == "ManufacturedItemDefinition":
        check_required(row.get("identifier"), "Identifier")
        check_numeric(row.get("unit_presentationID"), "Unit Presentation ID")
        check_numeric(row.get("doseFormID"), "Dose Form ID")
        check_spaces(row.get("identifier"), "Identifier")

    elif sheet == "MedicinalProductDefinition":
        check_required(row.get("productname"), "Product Name")
        check_required(row.get("ScientificNamePart"), "Scientific Name Part")
        check_required(row.get("StrengthPart"), "Strength Part")
        check_required(row.get("PharmaceuticalDosePart"), "Pharmaceutical Dose Part")
        check_required(row.get("country"), "Country")
        check_required(row.get("countryCode"), "Country Code")
        check_required(row.get("language"), "Language")
        check_required(row.get("languageID"), "Language ID")
        check_required(row.get("inventedNamePart"), "Invented Name Part")
        check_required(row.get("statusSuply"), "Status Supply")
        check_spaces(row.get("countryCode"), "Country Code")
        check_numeric(row.get("statusSuplyID"), "Status Supply ID")
        check_no_newline(row.get("productname"), "Product Name")
        check_no_newline(row.get("inventedNamePart"), "Invented Name Part")
        check_no_newline(row.get("ScientificNamePart"), "Scientific Name Part")
        check_no_newline(row.get("StrengthPart"), "Strength Part")
        check_no_newline(row.get("PharmaceuticalDosePart"), "Pharmaceutical Dose Part")

    elif sheet == "Organization":
        check_required(row.get("name"), "Name")
        check_required(row.get("type"), "Organization Type")
        check_required(row.get("identifier"), "Identifier")
        check_required(row.get("address_line"), "Address Line")
        check_required(row.get("address_city"), "City")
        check_required(row.get("address_country"), "Country")
        check_spaces(row.get("identifier"), "Identifier")
        check_numeric(row.get("address_postalCode"), "Postal Code")
        check_numeric(row.get("typeID"), "Type ID")
        check_no_newline(row.get("name"), "Name")

    elif sheet == "PackagedProductDefinition":
        check_required(row.get("name"), "Name")
        check_required(row.get("statusDate"), "Status Date")
        check_required(row.get("packaging_quantity"), "Packaging Quantity")
        check_required(row.get("packaging_identifier"), "Packaging Identifier")
        check_spaces(row.get("identifier"), "Identifier")
        check_numeric(row.get("packaging_quantity"), "Packaging Quantity")
        check_no_newline(row.get("name"), "Name")

    elif sheet == "Substance":
        check_required(row.get("name"), "Name")
        check_required(row.get("identifier"), "Identifier")
        check_no_newline(row.get("name"), "Name")
        check_spaces(row.get("identifier"), "Identifier")

    elif sheet == "ClinicalUseDefinition":
        check_required(row.get("type"), "Type")
        check_required(row.get("name"), "Name")
        check_required(row.get("conceptID"), "Concept ID")
        check_required(row.get("concept"), "Concept")
        check_no_newline(row.get("name"), "Name")
        check_spaces(row.get("identifier"), "Identifier")
        check_numeric(row.get("conceptID"), "Concept ID")
        if row.get("type") and row.get("type") not in ("Indication", "Contraindication", "Interaction"):
            errors.append("Type must be one of: Indication, Contraindication, Interaction")

    elif sheet == "Composition":
        check_required(row.get("language"), "Language")
        check_required(row.get("date"), "Date")
        check_required(row.get("name"), "Name")
        check_required(row.get("identifier_system"), "Identifier System")
        check_no_newline(row.get("name"), "Name")

    elif sheet == "RegulatedAuthorization":
        check_required(row.get("identifier"), "Identifier")
        check_required(row.get("statusDate"), "Status Date")
        check_required(row.get("reference"), "Reference")
        check_spaces(row.get("identifier"), "Identifier")
        if row.get("reference") and row.get("reference") not in ("MedicinalProduct", "PackagedProduct"):
            errors.append("Reference must be MedicinalProduct or PackagedProduct")
        if row.get("regionID") and str(row.get("regionID")).strip() != "":
            check_numeric(row.get("regionID"), "Region ID")

    elif sheet == "Bundle":
        check_required(row.get("language"), "Language")

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
        return False, [f"{sheet} has no entries yet."]
    blockers = []
    for i, row in enumerate(rows):
        for err in validate_row(row, sheet, session_data=session_data):
            blockers.append(f"Row {i + 1}: {err}")
    return (len(blockers) == 0), blockers


def validate_sheet_data(rows, sheet_name, session_data=None):
    all_errors = []
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
            errors.append(f"{sheet} is required. Please fill in the form.")

    singles = [
        "MedicinalProductDefinition",
        "ManufacturedItemDefinition",
        "AdministrableProductDefinition",
    ]
    for sheet in singles:
        if sheet in session_data and len(session_data[sheet]) > 1:
            errors.append(
                f"{sheet} must have exactly one entry. Found {len(session_data[sheet])}."
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
