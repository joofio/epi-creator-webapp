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

    _iso2_to_iso3 = {
        "AD": "AND", "AE": "ARE", "AF": "AFG", "AG": "ATG", "AI": "AIA", "AL": "ALB",
        "AM": "ARM", "AO": "AGO", "AQ": "ATA", "AR": "ARG", "AS": "ASM", "AT": "AUT",
        "AU": "AUS", "AW": "ABW", "AX": "ALA", "AZ": "AZE", "BA": "BIH", "BB": "BRB",
        "BD": "BGD", "BE": "BEL", "BF": "BFA", "BG": "BGR", "BH": "BHR", "BI": "BDI",
        "BJ": "BEN", "BL": "BLM", "BM": "BMU", "BN": "BRN", "BO": "BOL", "BQ": "BES",
        "BR": "BRA", "BS": "BHS", "BT": "BTN", "BV": "BVT", "BW": "BWA", "BY": "BLR",
        "BZ": "BLZ", "CA": "CAN", "CC": "CCK", "CD": "COD", "CF": "CAF", "CG": "COG",
        "CH": "CHE", "CI": "CIV", "CK": "COK", "CL": "CHL", "CM": "CMR", "CN": "CHN",
        "CO": "COL", "CR": "CRI", "CU": "CUB", "CV": "CPV", "CW": "CUW", "CX": "CXR",
        "CY": "CYP", "CZ": "CZE", "DE": "DEU", "DJ": "DJI", "DK": "DNK", "DM": "DMA",
        "DO": "DOM", "DZ": "DZA", "EC": "ECU", "EE": "EST", "EG": "EGY", "EH": "ESH",
        "ER": "ERI", "ES": "ESP", "ET": "ETH", "FI": "FIN", "FJ": "FJI", "FK": "FLK",
        "FM": "FSM", "FO": "FRO", "FR": "FRA", "GA": "GAB", "GB": "GBR", "GD": "GRD",
        "GE": "GEO", "GF": "GUF", "GG": "GGY", "GH": "GHA", "GI": "GIB", "GL": "GRL",
        "GM": "GMB", "GN": "GIN", "GP": "GLP", "GQ": "GNQ", "GR": "GRC", "GS": "SGS",
        "GT": "GTM", "GU": "GUM", "GW": "GNB", "GY": "GUY", "HK": "HKG", "HM": "HMD",
        "HN": "HND", "HR": "HRV", "HT": "HTI", "HU": "HUN", "ID": "IDN", "IE": "IRL",
        "IL": "ISR", "IM": "IMN", "IN": "IND", "IO": "IOT", "IQ": "IRQ", "IR": "IRN",
        "IS": "ISL", "IT": "ITA", "JE": "JEY", "JM": "JAM", "JO": "JOR", "JP": "JPN",
        "KE": "KEN", "KG": "KGZ", "KH": "KHM", "KI": "KIR", "KM": "COM", "KN": "KNA",
        "KP": "PRK", "KR": "KOR", "KW": "KWT", "KY": "CYM", "KZ": "KAZ", "LA": "LAO",
        "LB": "LBN", "LC": "LCA", "LI": "LIE", "LK": "LKA", "LR": "LBR", "LS": "LSO",
        "LT": "LTU", "LU": "LUX", "LV": "LVA", "LY": "LBY", "MA": "MAR", "MC": "MCO",
        "MD": "MDA", "ME": "MNE", "MF": "MAF", "MG": "MDG", "MH": "MHL", "MK": "MKD",
        "ML": "MLI", "MM": "MMR", "MN": "MNG", "MO": "MAC", "MP": "MNP", "MQ": "MTQ",
        "MR": "MRT", "MS": "MSR", "MT": "MLT", "MU": "MUS", "MV": "MDV", "MW": "MWI",
        "MX": "MEX", "MY": "MYS", "MZ": "MOZ", "NA": "NAM", "NC": "NCL", "NE": "NER",
        "NF": "NFK", "NG": "NGA", "NI": "NIC", "NL": "NLD", "NO": "NOR", "NP": "NPL",
        "NR": "NRU", "NU": "NIU", "NZ": "NZL", "OM": "OMN", "PA": "PAN", "PE": "PER",
        "PF": "PYF", "PG": "PNG", "PH": "PHL", "PK": "PAK", "PL": "POL", "PM": "SPM",
        "PN": "PCN", "PR": "PRI", "PS": "PSE", "PT": "PRT", "PW": "PLW", "PY": "PRY",
        "QA": "QAT", "RE": "REU", "RO": "ROU", "RS": "SRB", "RU": "RUS", "RW": "RWA",
        "SA": "SAU", "SB": "SLB", "SC": "SYC", "SD": "SDN", "SE": "SWE", "SG": "SGP",
        "SH": "SHN", "SI": "SVN", "SJ": "SJM", "SK": "SVK", "SL": "SLE", "SM": "SMR",
        "SN": "SEN", "SO": "SOM", "SR": "SUR", "SS": "SSD", "ST": "STP", "SV": "SLV",
        "SX": "SXM", "SY": "SYR", "SZ": "SWZ", "TC": "TCA", "TD": "TCD", "TF": "ATF",
        "TG": "TGO", "TH": "THA", "TJ": "TJK", "TK": "TKL", "TL": "TLS", "TM": "TKM",
        "TN": "TUN", "TO": "TON", "TR": "TUR", "TT": "TTO", "TV": "TUV", "TW": "TWN",
        "TZ": "TZA", "UA": "UKR", "UG": "UGA", "UM": "UMI", "US": "USA", "UY": "URY",
        "UZ": "UZB", "VA": "VAT", "VC": "VCT", "VE": "VEN", "VG": "VGB", "VI": "VIR",
        "VN": "VNM", "VU": "VUT", "WF": "WLF", "WS": "WSM", "YE": "YEM", "YT": "MYT",
        "ZA": "ZAF", "ZM": "ZMB", "ZW": "ZWE",
    }

    _countries = [
        ("AD", "Andorra"), ("AE", "United Arab Emirates"), ("AF", "Afghanistan"),
        ("AG", "Antigua and Barbuda"), ("AI", "Anguilla"), ("AL", "Albania"),
        ("AM", "Armenia"), ("AO", "Angola"), ("AQ", "Antarctica"), ("AR", "Argentina"),
        ("AS", "American Samoa"), ("AT", "Austria"), ("AU", "Australia"),
        ("AW", "Aruba"), ("AX", "Åland Islands"), ("AZ", "Azerbaijan"),
        ("BA", "Bosnia and Herzegovina"), ("BB", "Barbados"), ("BD", "Bangladesh"),
        ("BE", "Belgium"), ("BF", "Burkina Faso"), ("BG", "Bulgaria"),
        ("BH", "Bahrain"), ("BI", "Burundi"), ("BJ", "Benin"),
        ("BL", "Saint Barthélemy"), ("BM", "Bermuda"), ("BN", "Brunei Darussalam"),
        ("BO", "Bolivia"), ("BQ", "Bonaire, Sint Eustatius and Saba"), ("BR", "Brazil"),
        ("BS", "Bahamas"), ("BT", "Bhutan"), ("BV", "Bouvet Island"),
        ("BW", "Botswana"), ("BY", "Belarus"), ("BZ", "Belize"),
        ("CA", "Canada"), ("CC", "Cocos (Keeling) Islands"), ("CD", "Congo (Democratic Republic)"),
        ("CF", "Central African Republic"), ("CG", "Congo"), ("CH", "Switzerland"),
        ("CI", "Côte d'Ivoire"), ("CK", "Cook Islands"), ("CL", "Chile"),
        ("CM", "Cameroon"), ("CN", "China"), ("CO", "Colombia"),
        ("CR", "Costa Rica"), ("CU", "Cuba"), ("CV", "Cabo Verde"),
        ("CW", "Curaçao"), ("CX", "Christmas Island"), ("CY", "Cyprus"),
        ("CZ", "Czechia"), ("DE", "Germany"), ("DJ", "Djibouti"),
        ("DK", "Denmark"), ("DM", "Dominica"), ("DO", "Dominican Republic"),
        ("DZ", "Algeria"), ("EC", "Ecuador"), ("EE", "Estonia"),
        ("EG", "Egypt"), ("EH", "Western Sahara"), ("ER", "Eritrea"),
        ("ES", "Spain"), ("ET", "Ethiopia"), ("FI", "Finland"),
        ("FJ", "Fiji"), ("FK", "Falkland Islands (Malvinas)"), ("FM", "Micronesia"),
        ("FO", "Faroe Islands"), ("FR", "France"), ("GA", "Gabon"),
        ("GB", "United Kingdom"), ("GD", "Grenada"), ("GE", "Georgia"),
        ("GF", "French Guiana"), ("GG", "Guernsey"), ("GH", "Ghana"),
        ("GI", "Gibraltar"), ("GL", "Greenland"), ("GM", "Gambia"),
        ("GN", "Guinea"), ("GP", "Guadeloupe"), ("GQ", "Equatorial Guinea"),
        ("GR", "Greece"), ("GS", "South Georgia and the South Sandwich Islands"),
        ("GT", "Guatemala"), ("GU", "Guam"), ("GW", "Guinea-Bissau"),
        ("GY", "Guyana"), ("HK", "Hong Kong"), ("HM", "Heard Island and McDonald Islands"),
        ("HN", "Honduras"), ("HR", "Croatia"), ("HT", "Haiti"),
        ("HU", "Hungary"), ("ID", "Indonesia"), ("IE", "Ireland"),
        ("IL", "Israel"), ("IM", "Isle of Man"), ("IN", "India"),
        ("IO", "British Indian Ocean Territory"), ("IQ", "Iraq"), ("IR", "Iran"),
        ("IS", "Iceland"), ("IT", "Italy"), ("JE", "Jersey"),
        ("JM", "Jamaica"), ("JO", "Jordan"), ("JP", "Japan"),
        ("KE", "Kenya"), ("KG", "Kyrgyzstan"), ("KH", "Cambodia"),
        ("KI", "Kiribati"), ("KM", "Comoros"), ("KN", "Saint Kitts and Nevis"),
        ("KP", "Korea (North)"), ("KR", "Korea (South)"), ("KW", "Kuwait"),
        ("KY", "Cayman Islands"), ("KZ", "Kazakhstan"), ("LA", "Lao People's Democratic Republic"),
        ("LB", "Lebanon"), ("LC", "Saint Lucia"), ("LI", "Liechtenstein"),
        ("LK", "Sri Lanka"), ("LR", "Liberia"), ("LS", "Lesotho"),
        ("LT", "Lithuania"), ("LU", "Luxembourg"), ("LV", "Latvia"),
        ("LY", "Libya"), ("MA", "Morocco"), ("MC", "Monaco"),
        ("MD", "Moldova"), ("ME", "Montenegro"), ("MF", "Saint Martin (French part)"),
        ("MG", "Madagascar"), ("MH", "Marshall Islands"), ("MK", "North Macedonia"),
        ("ML", "Mali"), ("MM", "Myanmar"), ("MN", "Mongolia"),
        ("MO", "Macao"), ("MP", "Northern Mariana Islands"), ("MQ", "Martinique"),
        ("MR", "Mauritania"), ("MS", "Montserrat"), ("MT", "Malta"),
        ("MU", "Mauritius"), ("MV", "Maldives"), ("MW", "Malawi"),
        ("MX", "Mexico"), ("MY", "Malaysia"), ("MZ", "Mozambique"),
        ("NA", "Namibia"), ("NC", "New Caledonia"), ("NE", "Niger"),
        ("NF", "Norfolk Island"), ("NG", "Nigeria"), ("NI", "Nicaragua"),
        ("NL", "Netherlands"), ("NO", "Norway"), ("NP", "Nepal"),
        ("NR", "Nauru"), ("NU", "Niue"), ("NZ", "New Zealand"),
        ("OM", "Oman"), ("PA", "Panama"), ("PE", "Peru"),
        ("PF", "French Polynesia"), ("PG", "Papua New Guinea"), ("PH", "Philippines"),
        ("PK", "Pakistan"), ("PL", "Poland"), ("PM", "Saint Pierre and Miquelon"),
        ("PN", "Pitcairn"), ("PR", "Puerto Rico"), ("PS", "Palestine"),
        ("PT", "Portugal"), ("PW", "Palau"), ("PY", "Paraguay"),
        ("QA", "Qatar"), ("RE", "Réunion"), ("RO", "Romania"),
        ("RS", "Serbia"), ("RU", "Russian Federation"), ("RW", "Rwanda"),
        ("SA", "Saudi Arabia"), ("SB", "Solomon Islands"), ("SC", "Seychelles"),
        ("SD", "Sudan"), ("SE", "Sweden"), ("SG", "Singapore"),
        ("SH", "Saint Helena, Ascension and Tristan da Cunha"), ("SI", "Slovenia"),
        ("SJ", "Svalbard and Jan Mayen"), ("SK", "Slovakia"), ("SL", "Sierra Leone"),
        ("SM", "San Marino"), ("SN", "Senegal"), ("SO", "Somalia"),
        ("SR", "Suriname"), ("SS", "South Sudan"), ("ST", "Sao Tome and Principe"),
        ("SV", "El Salvador"), ("SX", "Sint Maarten (Dutch part)"), ("SY", "Syrian Arab Republic"),
        ("SZ", "Eswatini"), ("TC", "Turks and Caicos Islands"), ("TD", "Chad"),
        ("TF", "French Southern Territories"), ("TG", "Togo"), ("TH", "Thailand"),
        ("TJ", "Tajikistan"), ("TK", "Tokelau"), ("TL", "Timor-Leste"),
        ("TM", "Turkmenistan"), ("TN", "Tunisia"), ("TO", "Tonga"),
        ("TR", "Turkey"), ("TT", "Trinidad and Tobago"), ("TV", "Tuvalu"),
        ("TW", "Taiwan"), ("TZ", "Tanzania"), ("UA", "Ukraine"),
        ("UG", "Uganda"), ("UM", "United States Minor Outlying Islands"), ("US", "United States of America"),
        ("UY", "Uruguay"), ("UZ", "Uzbekistan"), ("VA", "Holy See"),
        ("VC", "Saint Vincent and the Grenadines"), ("VE", "Venezuela"), ("VG", "Virgin Islands (British)"),
        ("VI", "Virgin Islands (U.S.)"), ("VN", "Viet Nam"), ("VU", "Vanuatu"),
        ("WF", "Wallis and Futuna"), ("WS", "Samoa"), ("YE", "Yemen"),
        ("YT", "Mayotte"), ("ZA", "South Africa"), ("ZM", "Zambia"),
        ("ZW", "Zimbabwe"),
    ]

    _lookups["countriesWithCodes"] = [
        {"code": code, "id3": _iso2_to_iso3.get(code, ""), "name": name}
        for code, name in _countries
    ]
    _lookups["iso2to3"] = _iso2_to_iso3

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
