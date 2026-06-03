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

    _lookups["countriesWithCodes"] = [
        {"code": "AD", "name": "Andorra"},
        {"code": "AE", "name": "United Arab Emirates"},
        {"code": "AF", "name": "Afghanistan"},
        {"code": "AG", "name": "Antigua and Barbuda"},
        {"code": "AI", "name": "Anguilla"},
        {"code": "AL", "name": "Albania"},
        {"code": "AM", "name": "Armenia"},
        {"code": "AO", "name": "Angola"},
        {"code": "AQ", "name": "Antarctica"},
        {"code": "AR", "name": "Argentina"},
        {"code": "AS", "name": "American Samoa"},
        {"code": "AT", "name": "Austria"},
        {"code": "AU", "name": "Australia"},
        {"code": "AW", "name": "Aruba"},
        {"code": "AX", "name": "Åland Islands"},
        {"code": "AZ", "name": "Azerbaijan"},
        {"code": "BA", "name": "Bosnia and Herzegovina"},
        {"code": "BB", "name": "Barbados"},
        {"code": "BD", "name": "Bangladesh"},
        {"code": "BE", "name": "Belgium"},
        {"code": "BF", "name": "Burkina Faso"},
        {"code": "BG", "name": "Bulgaria"},
        {"code": "BH", "name": "Bahrain"},
        {"code": "BI", "name": "Burundi"},
        {"code": "BJ", "name": "Benin"},
        {"code": "BL", "name": "Saint Barthélemy"},
        {"code": "BM", "name": "Bermuda"},
        {"code": "BN", "name": "Brunei Darussalam"},
        {"code": "BO", "name": "Bolivia"},
        {"code": "BQ", "name": "Bonaire, Sint Eustatius and Saba"},
        {"code": "BR", "name": "Brazil"},
        {"code": "BS", "name": "Bahamas"},
        {"code": "BT", "name": "Bhutan"},
        {"code": "BV", "name": "Bouvet Island"},
        {"code": "BW", "name": "Botswana"},
        {"code": "BY", "name": "Belarus"},
        {"code": "BZ", "name": "Belize"},
        {"code": "CA", "name": "Canada"},
        {"code": "CC", "name": "Cocos (Keeling) Islands"},
        {"code": "CD", "name": "Congo (Democratic Republic)"},
        {"code": "CF", "name": "Central African Republic"},
        {"code": "CG", "name": "Congo"},
        {"code": "CH", "name": "Switzerland"},
        {"code": "CI", "name": "Côte d'Ivoire"},
        {"code": "CK", "name": "Cook Islands"},
        {"code": "CL", "name": "Chile"},
        {"code": "CM", "name": "Cameroon"},
        {"code": "CN", "name": "China"},
        {"code": "CO", "name": "Colombia"},
        {"code": "CR", "name": "Costa Rica"},
        {"code": "CU", "name": "Cuba"},
        {"code": "CV", "name": "Cabo Verde"},
        {"code": "CW", "name": "Curaçao"},
        {"code": "CX", "name": "Christmas Island"},
        {"code": "CY", "name": "Cyprus"},
        {"code": "CZ", "name": "Czechia"},
        {"code": "DE", "name": "Germany"},
        {"code": "DJ", "name": "Djibouti"},
        {"code": "DK", "name": "Denmark"},
        {"code": "DM", "name": "Dominica"},
        {"code": "DO", "name": "Dominican Republic"},
        {"code": "DZ", "name": "Algeria"},
        {"code": "EC", "name": "Ecuador"},
        {"code": "EE", "name": "Estonia"},
        {"code": "EG", "name": "Egypt"},
        {"code": "EH", "name": "Western Sahara"},
        {"code": "ER", "name": "Eritrea"},
        {"code": "ES", "name": "Spain"},
        {"code": "ET", "name": "Ethiopia"},
        {"code": "FI", "name": "Finland"},
        {"code": "FJ", "name": "Fiji"},
        {"code": "FK", "name": "Falkland Islands (Malvinas)"},
        {"code": "FM", "name": "Micronesia"},
        {"code": "FO", "name": "Faroe Islands"},
        {"code": "FR", "name": "France"},
        {"code": "GA", "name": "Gabon"},
        {"code": "GB", "name": "United Kingdom"},
        {"code": "GD", "name": "Grenada"},
        {"code": "GE", "name": "Georgia"},
        {"code": "GF", "name": "French Guiana"},
        {"code": "GG", "name": "Guernsey"},
        {"code": "GH", "name": "Ghana"},
        {"code": "GI", "name": "Gibraltar"},
        {"code": "GL", "name": "Greenland"},
        {"code": "GM", "name": "Gambia"},
        {"code": "GN", "name": "Guinea"},
        {"code": "GP", "name": "Guadeloupe"},
        {"code": "GQ", "name": "Equatorial Guinea"},
        {"code": "GR", "name": "Greece"},
        {"code": "GS", "name": "South Georgia and the South Sandwich Islands"},
        {"code": "GT", "name": "Guatemala"},
        {"code": "GU", "name": "Guam"},
        {"code": "GW", "name": "Guinea-Bissau"},
        {"code": "GY", "name": "Guyana"},
        {"code": "HK", "name": "Hong Kong"},
        {"code": "HM", "name": "Heard Island and McDonald Islands"},
        {"code": "HN", "name": "Honduras"},
        {"code": "HR", "name": "Croatia"},
        {"code": "HT", "name": "Haiti"},
        {"code": "HU", "name": "Hungary"},
        {"code": "ID", "name": "Indonesia"},
        {"code": "IE", "name": "Ireland"},
        {"code": "IL", "name": "Israel"},
        {"code": "IM", "name": "Isle of Man"},
        {"code": "IN", "name": "India"},
        {"code": "IO", "name": "British Indian Ocean Territory"},
        {"code": "IQ", "name": "Iraq"},
        {"code": "IR", "name": "Iran"},
        {"code": "IS", "name": "Iceland"},
        {"code": "IT", "name": "Italy"},
        {"code": "JE", "name": "Jersey"},
        {"code": "JM", "name": "Jamaica"},
        {"code": "JO", "name": "Jordan"},
        {"code": "JP", "name": "Japan"},
        {"code": "KE", "name": "Kenya"},
        {"code": "KG", "name": "Kyrgyzstan"},
        {"code": "KH", "name": "Cambodia"},
        {"code": "KI", "name": "Kiribati"},
        {"code": "KM", "name": "Comoros"},
        {"code": "KN", "name": "Saint Kitts and Nevis"},
        {"code": "KP", "name": "Korea (North)"},
        {"code": "KR", "name": "Korea (South)"},
        {"code": "KW", "name": "Kuwait"},
        {"code": "KY", "name": "Cayman Islands"},
        {"code": "KZ", "name": "Kazakhstan"},
        {"code": "LA", "name": "Lao People's Democratic Republic"},
        {"code": "LB", "name": "Lebanon"},
        {"code": "LC", "name": "Saint Lucia"},
        {"code": "LI", "name": "Liechtenstein"},
        {"code": "LK", "name": "Sri Lanka"},
        {"code": "LR", "name": "Liberia"},
        {"code": "LS", "name": "Lesotho"},
        {"code": "LT", "name": "Lithuania"},
        {"code": "LU", "name": "Luxembourg"},
        {"code": "LV", "name": "Latvia"},
        {"code": "LY", "name": "Libya"},
        {"code": "MA", "name": "Morocco"},
        {"code": "MC", "name": "Monaco"},
        {"code": "MD", "name": "Moldova"},
        {"code": "ME", "name": "Montenegro"},
        {"code": "MF", "name": "Saint Martin (French part)"},
        {"code": "MG", "name": "Madagascar"},
        {"code": "MH", "name": "Marshall Islands"},
        {"code": "MK", "name": "North Macedonia"},
        {"code": "ML", "name": "Mali"},
        {"code": "MM", "name": "Myanmar"},
        {"code": "MN", "name": "Mongolia"},
        {"code": "MO", "name": "Macao"},
        {"code": "MP", "name": "Northern Mariana Islands"},
        {"code": "MQ", "name": "Martinique"},
        {"code": "MR", "name": "Mauritania"},
        {"code": "MS", "name": "Montserrat"},
        {"code": "MT", "name": "Malta"},
        {"code": "MU", "name": "Mauritius"},
        {"code": "MV", "name": "Maldives"},
        {"code": "MW", "name": "Malawi"},
        {"code": "MX", "name": "Mexico"},
        {"code": "MY", "name": "Malaysia"},
        {"code": "MZ", "name": "Mozambique"},
        {"code": "NA", "name": "Namibia"},
        {"code": "NC", "name": "New Caledonia"},
        {"code": "NE", "name": "Niger"},
        {"code": "NF", "name": "Norfolk Island"},
        {"code": "NG", "name": "Nigeria"},
        {"code": "NI", "name": "Nicaragua"},
        {"code": "NL", "name": "Netherlands"},
        {"code": "NO", "name": "Norway"},
        {"code": "NP", "name": "Nepal"},
        {"code": "NR", "name": "Nauru"},
        {"code": "NU", "name": "Niue"},
        {"code": "NZ", "name": "New Zealand"},
        {"code": "OM", "name": "Oman"},
        {"code": "PA", "name": "Panama"},
        {"code": "PE", "name": "Peru"},
        {"code": "PF", "name": "French Polynesia"},
        {"code": "PG", "name": "Papua New Guinea"},
        {"code": "PH", "name": "Philippines"},
        {"code": "PK", "name": "Pakistan"},
        {"code": "PL", "name": "Poland"},
        {"code": "PM", "name": "Saint Pierre and Miquelon"},
        {"code": "PN", "name": "Pitcairn"},
        {"code": "PR", "name": "Puerto Rico"},
        {"code": "PS", "name": "Palestine"},
        {"code": "PT", "name": "Portugal"},
        {"code": "PW", "name": "Palau"},
        {"code": "PY", "name": "Paraguay"},
        {"code": "QA", "name": "Qatar"},
        {"code": "RE", "name": "Réunion"},
        {"code": "RO", "name": "Romania"},
        {"code": "RS", "name": "Serbia"},
        {"code": "RU", "name": "Russian Federation"},
        {"code": "RW", "name": "Rwanda"},
        {"code": "SA", "name": "Saudi Arabia"},
        {"code": "SB", "name": "Solomon Islands"},
        {"code": "SC", "name": "Seychelles"},
        {"code": "SD", "name": "Sudan"},
        {"code": "SE", "name": "Sweden"},
        {"code": "SG", "name": "Singapore"},
        {"code": "SH", "name": "Saint Helena, Ascension and Tristan da Cunha"},
        {"code": "SI", "name": "Slovenia"},
        {"code": "SJ", "name": "Svalbard and Jan Mayen"},
        {"code": "SK", "name": "Slovakia"},
        {"code": "SL", "name": "Sierra Leone"},
        {"code": "SM", "name": "San Marino"},
        {"code": "SN", "name": "Senegal"},
        {"code": "SO", "name": "Somalia"},
        {"code": "SR", "name": "Suriname"},
        {"code": "SS", "name": "South Sudan"},
        {"code": "ST", "name": "Sao Tome and Principe"},
        {"code": "SV", "name": "El Salvador"},
        {"code": "SX", "name": "Sint Maarten (Dutch part)"},
        {"code": "SY", "name": "Syrian Arab Republic"},
        {"code": "SZ", "name": "Eswatini"},
        {"code": "TC", "name": "Turks and Caicos Islands"},
        {"code": "TD", "name": "Chad"},
        {"code": "TF", "name": "French Southern Territories"},
        {"code": "TG", "name": "Togo"},
        {"code": "TH", "name": "Thailand"},
        {"code": "TJ", "name": "Tajikistan"},
        {"code": "TK", "name": "Tokelau"},
        {"code": "TL", "name": "Timor-Leste"},
        {"code": "TM", "name": "Turkmenistan"},
        {"code": "TN", "name": "Tunisia"},
        {"code": "TO", "name": "Tonga"},
        {"code": "TR", "name": "Turkey"},
        {"code": "TT", "name": "Trinidad and Tobago"},
        {"code": "TV", "name": "Tuvalu"},
        {"code": "TW", "name": "Taiwan"},
        {"code": "TZ", "name": "Tanzania"},
        {"code": "UA", "name": "Ukraine"},
        {"code": "UG", "name": "Uganda"},
        {"code": "UM", "name": "United States Minor Outlying Islands"},
        {"code": "US", "name": "United States of America"},
        {"code": "UY", "name": "Uruguay"},
        {"code": "UZ", "name": "Uzbekistan"},
        {"code": "VA", "name": "Holy See"},
        {"code": "VC", "name": "Saint Vincent and the Grenadines"},
        {"code": "VE", "name": "Venezuela"},
        {"code": "VG", "name": "Virgin Islands (British)"},
        {"code": "VI", "name": "Virgin Islands (U.S.)"},
        {"code": "VN", "name": "Viet Nam"},
        {"code": "VU", "name": "Vanuatu"},
        {"code": "WF", "name": "Wallis and Futuna"},
        {"code": "WS", "name": "Samoa"},
        {"code": "YE", "name": "Yemen"},
        {"code": "YT", "name": "Mayotte"},
        {"code": "ZA", "name": "South Africa"},
        {"code": "ZM", "name": "Zambia"},
        {"code": "ZW", "name": "Zimbabwe"},
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
