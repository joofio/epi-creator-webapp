import pandas as pd
import os

_lookups = {}


def load_lookups(excel_path="acmeDrug_1.xlsx"):
    if not os.path.exists(excel_path):
        print(f"WARNING: lookup file {excel_path} not found, lookups will be empty")
        return

    extra = pd.read_excel(excel_path, sheet_name="EXTRA")
    data_val = pd.read_excel(excel_path, sheet_name="DATA_VAL")

    _lookups["doseForms"] = sorted(
        extra["100000072057_descr"].dropna().unique().tolist()
    )

    _lookups["routes"] = sorted(
        extra["100000073345_descr"].dropna().unique().tolist()
    )

    _lookups["unitPresentations"] = sorted(
        extra["100000000002_descr"].dropna().unique().tolist()
    )

    _lookups["countries"] = sorted(
        extra["sms_descr"].dropna().apply(
            lambda x: x if isinstance(x, str) and len(x) < 50 else None
        ).dropna().unique().tolist()
    )

    _lookups["orgTypes"] = [
        "Marketing Authorisation Holder",
        "Medicines Regulatory Authority",
        "Manufacturer",
        "Master File Holder",
        "Contact Location",
        "Manufacturer Batch Release",
        "Manufacturer API",
    ]

    _lookups["substances"] = sorted(
        extra["sms_descr"].dropna().unique().tolist()
    )

    _lookups["packagingTypes"] = [
        "Blister", "Bottle", "Carton", "Vial", "Ampoule",
        "Tube", "Sachet", "Syringe", "Bag", "Jar",
        "Pre-filled pen", "Pre-filled syringe",
        "Container", "Box", "Pouch", "Strip",
    ]

    _lookups["packagingMaterials"] = [
        "PVC", "Aluminium", "Glass", "HDPE", "LDPE",
        "PET", "Paper", "Cardboard", "PVC/PVDC",
        "Aluminium/PVC", "Polypropylene", "Polystyrene",
    ]

    _lookups["languages"] = [
        {"code": "en", "name": "English"},
        {"code": "pt", "name": "Portuguese"},
        {"code": "es", "name": "Spanish"},
        {"code": "fr", "name": "French"},
        {"code": "de", "name": "German"},
        {"code": "it", "name": "Italian"},
        {"code": "nl", "name": "Dutch"},
        {"code": "el", "name": "Greek"},
        {"code": "sv", "name": "Swedish"},
        {"code": "da", "name": "Danish"},
        {"code": "fi", "name": "Finnish"},
        {"code": "no", "name": "Norwegian"},
        {"code": "pl", "name": "Polish"},
        {"code": "cs", "name": "Czech"},
        {"code": "hu", "name": "Hungarian"},
        {"code": "ro", "name": "Romanian"},
        {"code": "bg", "name": "Bulgarian"},
        {"code": "hr", "name": "Croatian"},
        {"code": "lt", "name": "Lithuanian"},
        {"code": "lv", "name": "Latvian"},
        {"code": "et", "name": "Estonian"},
        {"code": "sk", "name": "Slovak"},
        {"code": "sl", "name": "Slovenian"},
        {"code": "mt", "name": "Maltese"},
        {"code": "ga", "name": "Irish"},
        {"code": "is", "name": "Icelandic"},
    ]

    _lookups["statusSupply"] = [
        {"id": "100000072078", "text": "No information available"},
        {"id": "100000072079", "text": "Never valid"},
        {"id": "100000072080", "text": "No supplied"},
        {"id": "100000072081", "text": "Valid"},
        {"id": "100000072082", "text": "Withdrawn"},
        {"id": "100000072083", "text": "Expired"},
        {"id": "100000072084", "text": "Suspended"},
        {"id": "100000072164", "text": "Not ongoing"},
        {"id": "100000072170", "text": "Ongoing but no marketing authorisation issued"},
        {"id": "200000019455", "text": "Renewed"},
        {"id": "200000019456", "text": "Revoked"},
        {"id": "200000019457", "text": "Refused"},
        {"id": "200000019458", "text": "Transferred"},
    ]

    _lookups["orgTypeIDs"] = {
        "Marketing Authorisation Holder": "220000000008",
        "Medicines Regulatory Authority": "220000000032",
        "Manufacturer": "220000000033",
        "Master File Holder": "220000000034",
        "Contact Location": "220000000035",
        "Manufacturer Batch Release": "220000000036",
        "Manufacturer API": "220000000037",
    }

    _lookups["ingredientRoles"] = [
        {"id": "100000072070", "name": "Active"},
        {"id": "100000072071", "name": "Adjuvant"},
        {"id": "100000072072", "name": "Excipient"},
        {"id": "100000072082", "name": "Solvent / Diluent"},
    ]

    _lookups["classificationItems"] = sorted(
        extra["100000155526_descr"].dropna().unique().tolist()
    )

    _lookups["clinicalUseTypes"] = ["indication", "contraindication", "interaction"]

    _lookups["doseFormIDLookup"] = {}
    for _, row in extra.iterrows():
        code = row.get("100000072057")
        desc = row.get("100000072057_descr")
        if pd.notna(code) and pd.notna(desc):
            _lookups["doseFormIDLookup"][str(desc)] = str(int(code))

    _lookups["routeIDLookup"] = {}
    for _, row in extra.iterrows():
        code = row.get("100000073345")
        desc = row.get("100000073345_descr")
        if pd.notna(code) and pd.notna(desc):
            _lookups["routeIDLookup"][str(desc)] = str(int(code))

    _lookups["unitPresentationIDLookup"] = {}
    for _, row in extra.iterrows():
        code = row.get("100000000002")
        desc = row.get("100000000002_descr")
        if pd.notna(code) and pd.notna(desc):
            _lookups["unitPresentationIDLookup"][str(desc)] = str(int(code))

    print(f"lookup.py: Loaded {len(_lookups)} lookup categories")


def get_lookups():
    return _lookups


def get_lookup(category):
    return _lookups.get(category, [])


def get_category_id(category, description):
    lookup_map = {
        "doseForm": "doseFormIDLookup",
        "route": "routeIDLookup",
        "unitPresentation": "unitPresentationIDLookup",
    }
    key = lookup_map.get(category)
    if key and key in _lookups:
        return _lookups[key].get(description, "")
    return ""
