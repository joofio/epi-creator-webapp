import pandas as pd
import os

_lookups = {}
_loaded = False


def load_lookups(excel_path="acmeDrug_1.xlsx"):
    global _loaded
    if _loaded:
        return
    _loaded = True
    if not os.path.exists(excel_path):
        print(f"WARNING: lookup file {excel_path} not found, lookups will be empty")
        return

    extra = pd.read_excel(excel_path, sheet_name="EXTRA")
    data_val = pd.read_excel(excel_path, sheet_name="DATA_VAL")

    _lookups["doseForms"] = sorted(
        extra["200000000004_descr"].dropna().unique().tolist()
    )

    _lookups["routes"] = sorted(
        extra["100000073345_descr"].dropna().unique().tolist()
    )

    _lookups["unitPresentations"] = sorted(
        extra["200000000014_descr"].dropna().unique().tolist()
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

    _lookups["packagingTypes"] = sorted(
        extra["100000073346_descr"].dropna().unique().tolist()
    )

    _lookups["packagingMaterials"] = sorted(
        extra["200000003199_descr"].dropna().unique().tolist()
    )

    _lookups["packagedProductTypes"] = sorted(
        extra["100000155526_descr"].dropna().unique().tolist()
    )

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

    _lookups["authorizationTypes"] = [
        {"id": "220000000061", "name": "Marketing Authorisation"},
        {"id": "220000000062", "name": "Orphan Designation"},
        {"id": "220000000063", "name": "Parallel Trade Approval"},
        {"id": "220000000064", "name": "Minor Use Minor Species"},
        {"id": "220000000065", "name": "Paediatric Investigational Plan"},
        {"id": "200000015756", "name": "Homeopathic Registration"},
        {"id": "200000016178", "name": "Exemption for veterinary medicinal products"},
    ]

    _lookups["classificationItems"] = sorted(
        extra["100000155526_descr"].dropna().unique().tolist()
    )

    _lookups["clinicalUseTypes"] = ["indication", "contraindication", "interaction"]

    _lookups["doseFormIDLookup"] = {}
    for _, row in extra.iterrows():
        code = row.get("200000000004")
        desc = row.get("200000000004_descr")
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
        code = row.get("200000000014")
        desc = row.get("200000000014_descr")
        if pd.notna(code) and pd.notna(desc):
            _lookups["unitPresentationIDLookup"][str(desc)] = str(int(code))

    _lookups["packagedProductTypeIDLookup"] = {}
    for _, row in extra.iterrows():
        code = row.get(100000155526)
        desc = row.get("100000155526_descr")
        if pd.notna(code) and pd.notna(desc):
            _lookups["packagedProductTypeIDLookup"][str(desc)] = str(int(code))

    _lookups["packagingTypeIDLookup"] = {}
    for _, row in extra.iterrows():
        code = row.get("100000073346")
        desc = row.get("100000073346_descr")
        if pd.notna(code) and pd.notna(desc):
            _lookups["packagingTypeIDLookup"][str(desc)] = str(int(code))

    _lookups["packagingMaterialIDLookup"] = {}
    for _, row in extra.iterrows():
        code = row.get("200000003199")
        desc = row.get("200000003199_descr")
        if pd.notna(code) and pd.notna(desc):
            _lookups["packagingMaterialIDLookup"][str(desc)] = str(int(code))

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
