def validate_row(row, sheet):
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
        check_spaces(row.get("status"), "Status")
        check_numeric(row.get("unit_presentationID"), "Unit Presentation ID")
        check_numeric(row.get("routeID"), "Route ID")
        check_numeric(row.get("doseFormID"), "Dose Form ID")
        check_no_newline(row.get("name"), "Name")

    elif sheet == "Ingredient":
        check_spaces(row.get("identifier"), "Identifier")
        check_spaces(row.get("StrengthBasis"), "Strength Basis")
        check_numeric(row.get("quantity"), "Quantity")
        check_numeric(row.get("roleID"), "Role ID")
        check_no_newline(row.get("name"), "Name")
        role = (row.get("role") or "").lower()
        if role in ("active", "ativo"):
            if not row.get("StrengthBasis") or str(row.get("StrengthBasis")).strip() == "":
                errors.append("Strength Basis is required for active ingredients")
            if not row.get("quantity") or str(row.get("quantity")).strip() == "":
                errors.append("Quantity is required for active ingredients")

    elif sheet == "ManufacturedItemDefinition":
        check_spaces(row.get("status"), "Status")
        check_numeric(row.get("unit_presentationID"), "Unit Presentation ID")
        check_numeric(row.get("doseFormID"), "Dose Form ID")
        check_no_newline(row.get("name"), "Name")
        check_spaces(row.get("identifier"), "Identifier")

    elif sheet == "MedicinalProductDefinition":
        check_no_newline(row.get("productname"), "Product Name")
        check_spaces(row.get("status"), "Status")
        check_spaces(row.get("countryCode"), "Country Code")
        check_numeric(row.get("statusSuplyID"), "Status Supply ID")
        check_no_newline(row.get("inventedNamePart"), "Invented Name Part")
        check_no_newline(row.get("ScientificNamePart"), "Scientific Name Part")
        check_no_newline(row.get("StrengthPart"), "Strength Part")
        check_no_newline(row.get("PharmaceuticalDosePart"), "Pharmaceutical Dose Part")

    elif sheet == "Organization":
        check_spaces(row.get("identifier"), "Identifier")
        check_numeric(row.get("address_postalCode"), "Postal Code")
        check_numeric(row.get("typeID"), "Type ID")
        check_no_newline(row.get("name"), "Name")

    elif sheet == "PackagedProductDefinition":
        check_spaces(row.get("identifier"), "Identifier")
        check_numeric(row.get("inside_packaging_typeID"), "Inside Packaging Type ID")
        check_numeric(row.get("inside_packaging_quantity"), "Inside Packaging Quantity")
        check_numeric(row.get("packaging_quantity"), "Packaging Quantity")
        check_numeric(row.get("Packaging_typeID"), "Packaging Type ID")
        check_numeric(row.get("packaging_materialID"), "Packaging Material ID")
        check_numeric(row.get("typeID"), "Type ID")
        check_no_newline(row.get("name"), "Name")

    elif sheet == "Substance":
        check_no_newline(row.get("name"), "Name")
        check_spaces(row.get("identifier"), "Identifier")

    elif sheet == "ClinicalUseDefinition":
        check_no_newline(row.get("name"), "Name")
        check_spaces(row.get("identifier"), "Identifier")
        check_numeric(row.get("conceptID"), "Concept ID")

    elif sheet == "Composition":
        check_no_newline(row.get("name"), "Name")
        if not row.get("language") or str(row.get("language")).strip() == "":
            errors.append("Language is required")

    elif sheet == "RegulatedAuthorization":
        check_spaces(row.get("identifier"), "Identifier")
        check_numeric(row.get("typeID"), "Type ID")
        if row.get("regionID") and str(row.get("regionID")).strip() != "":
            check_numeric(row.get("regionID"), "Region ID")

    elif sheet == "Bundle":
        if not row.get("language") or str(row.get("language")).strip() == "":
            errors.append("Language is required")

    return errors


def validate_sheet_data(rows, sheet_name):
    all_errors = []
    for idx, row in enumerate(rows):
        errs = validate_row(row, sheet_name)
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

    orgs = session_data.get("Organization", [])
    has_mah = any(
        (r.get("type") or "").lower() == "marketing authorisation holder"
        for r in orgs
    )
    if not has_mah:
        errors.append("At least one Marketing Authorisation Holder organization is required.")

    return errors
