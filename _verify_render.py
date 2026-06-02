"""Smoke test: render FSH from sample session data and run SUSHI."""
import os
import sys
import shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from epi_creator.lookup import load_lookups
from epi_creator.functions import create_from_session, create_env

load_lookups()

OUTPUT_FOLDER = "input/fsh/examples"


def main():
    if os.path.exists(OUTPUT_FOLDER):
        shutil.rmtree(OUTPUT_FOLDER)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    session_data = {
        "Organization": [
            {
                "name": "Acme Pharma",
                "identifier": "ORG-001",
                "type": "Marketing Authorisation Holder",
                "typeID": "220000000008",
                "address_line": "123 Main St",
                "address_city": "Lisbon",
                "address_country": "PT",
                "address_postalCode": "1000",
            }
        ],
        "MedicinalProductDefinition": [
            {
                "productname": "AcmeDrug",
                "inventedNamePart": "AcmeDrug",
                "ScientificNamePart": "acmecillin",
                "StrengthPart": "500 mg",
                "PharmaceuticalDosePart": "tablet",
                "country": "Portugal",
                "countryCode": "PT",
                "language": "English",
                "languageID": "en",
                "statusSuply": "Valid",
                "statusSuplyID": "100000072081",
                "identifier_system": "https://spor.ema.europa.eu/pmswi",
                "identifier_value": "EU/1/97/049/001",
                "classification_ids": "200000025003",
                "classification_texts": "Chemical",
                "indication": "Hypertension",
            }
        ],
        "Substance": [
            {
                "name": "acmecillin",
                "identifier": "SUB-001",
                "version": "1",
                "description": "Active substance",
                "moleclularWeigth": "500.5",
                "moleclularWeigthType": "base",
                "molecularFormula": "C22H30N6O4S",
                "name_name": "Acmecillin",
                "name_type": "INN",
                "name_typeID": "100000072070",
            }
        ],
        "Ingredient": [
            {
                "name": "acmecillin",
                "role": "Active",
                "identifier": "SUB-001",
                "StrengthBasis": "active-moiety",
                "StrengthBasisText": "Active moiety",
                "quantity": "500",
                "quantity unit": "mg",
            }
        ],
        "RegulatedAuthorization": [
            {
                "identifier": "REG-001",
                "statusDate": "2024-01-01",
                "type": "Marketing Authorisation",
                "typeID": "220000000061",
                "reference": "EU/1/97/049/001",
                "region": "EU",
                "regionID": "EU",
            }
        ],
        "ManufacturedItemDefinition": [
            {
                "identifier": "MAN-001",
                "doseForm": "Tablet",
                "doseFormID": "100000073654",
                "unit_presentation": "Tablet",
                "unit_presentationID": "200000002004",
            }
        ],
        "AdministrableProductDefinition": [
            {
                "identifier": "ADM-001",
                "doseForm": "Tablet",
                "doseFormID": "100000073654",
                "unit_presentation": "Tablet",
                "unit_presentationID": "200000002004",
                "route": "Oral",
                "routeID": "100000073345",
            }
        ],
        "PackagedProductDefinition": [
            {
                "name": "AcmeDrug 500mg",
                "identifier": "PPD-001",
                "type": "Chemical Medicinal Product",
                "typeID": "100000155527",
                "statusDate": "2024-01-01",
                "quantity": "28 tablet",
                "packaging_quantity": "1",
                "packaging_identifier": "PKG-001",
                "Packaging_type": "Blister",
                "Packaging_typeID": "100000073498",
                "packaging_material": "Aluminium",
                "packaging_materialID": "",
                "description": "28 tablets in a blister",
                "copackagedIndicator": "false",
            }
        ],
        "ClinicalUseDefinition": [],
        "Composition": [
            {
                "name": "AcmeDrug leaflet",
                "language": "en",
                "date": "2024-01-01",
                "identifier_system": "https://spor.ema.europa.eu/pmswi",
                "identifier": "LEAFLET-001",
                "package_leaflet": "...",
                "information_user": "...",
                "what_in_leaflet": "...",
                "what_product_is": "...",
                "before_take": "...",
                "how_to_take": "...",
                "side_effects": "...",
                "how_to_store": "...",
                "other_info": "...",
            }
        ],
        "Bundle": [
            {
                "language": "en",
                "identifier_system": "https://spor.ema.europa.eu/pmswi",
                "identifier_value": "AcmeDrug-bundle",
            }
        ],
    }

    env = create_env("templates/")
    create_from_session(env, session_data, "templates/", OUTPUT_FOLDER, "acme")
    print("FSH regenerated.")


if __name__ == "__main__":
    main()
