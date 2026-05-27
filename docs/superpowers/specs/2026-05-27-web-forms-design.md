# Design Spec: Replace Excel Input with Web Forms

## 1. Goal

Replace the Excel-centric workflow with interactive web forms that follow the same 11-sheet structure, generating FHIR Shorthand and JSON identically to the current process. Remove all Excel parsing, remove CSV intermediate files, and add proper client/server validation.

## 2. Architecture

**Stack:** Flask + Jinja2 + htmx + Alpine.js — no build step, no SPA framework.

**Key principle:** `functions.py` changes minimally. Instead of reading Excel → pandas → Jinja2, it receives a session dict → builds DataFrames in memory → runs the same two-pass Jinja2 render → calls sushi.

**New module structure:**

```
epi_creator/
  __init__.py              # Session config, blueprints
  views.py                 # Wizard routes, generate, download, lookup API
  functions.py             # Refactored: accepts dict instead of Excel path
  validator.py             # Reactivated + expanded
  lookup.py                # NEW: loads EXTRA/DATA_VAL at startup, serves JSON
  static/
    css/main.css
    js/autocomplete.js     # Alpine.js autocomplete component
    js/validator.js        # Client-side validation helpers
  templates/
    index.html             # Updated landing (no upload, just "Start" button)
    faq.html               # Unchanged
    wizard/
      base.html            # Wizard layout: sidebar + main content
      _sidebar.html        # Progress sidebar partial (htmx OOB swap)
      organization.html
      medicinal_product.html
      substance.html
      ingredient.html
      regulated_auth.html
      manufactured_item.html
      administrable_product.html
      packaged_product.html
      clinical_use.html
      composition.html
      bundle.html
```

**What stays unchanged:**
- All 11 FSH templates in `/templates/`
- `input/fsh/aliases.fsh`
- `sushi-config.yaml`
- `Dockerfile` and `gunicorn.sh`
- Two-pass render logic (just input source changes)
- Zip/download packaging

**What stays (for lookup data only):**
- `acmeDrug.xlsx` — kept solely as the source for EXTRA and DATA_VAL lookup sheets, loaded once at startup by `lookup.py`. Not served as a template download.

**What gets removed:**
- `/upload` route (POST multipart)
- `/download?filename=acmeDrug.xlsx` (Excel template download)
- `pd.read_excel()` calls in the user-input path
- CSV intermediate writes to temp/

## 3. Navigation: Hybrid Wizard + Sidebar

- Sequential flow: Organization → Bundle (11 steps)
- Sidebar shows all steps with status: done / current / pending
- Completed steps are clickable to jump back
- Not-yet-reached steps are greyed/disabled
- Sidebar is a Jinja partial, re-rendered via htmx OOB swap after each POST
- Step order: Organization, MedicinalProduct, Substance, Ingredient, RegulatedAuthorization, ManufacturedItem, AdministrableProduct, PackagedProduct, ClinicalUse, Composition, Bundle

## 4. Session Data Model

```python
session["data"] = {
    "Organization": [
        {"id": "ORG-001", "name": "Acme Inc", "type": "mah", ...},
    ],
    "MedicinalProductDefinition": [
        {"productname": "AcmeDrug", ...},  # single row list
    ],
    "Substance": [...],
    "Ingredient": [...],
    "RegulatedAuthorization": [...],
    "ManufacturedItemDefinition": [...],
    "AdministrableProductDefinition": [...],
    "PackagedProductDefinition": [...],
    "ClinicalUseDefinition": [...],
    "Composition": [...],
    "Bundle": [...],
}
```

Singletons stored as 1-element lists so existing `iterrows()` loops work unchanged. Each row is a dict with column names matching the Excel headers.

## 5. Form Categories & Interaction Patterns

### Single-entry forms (simple labeled fields)
**MedicinalProductDefinition, ManufacturedItemDefinition, AdministrableProductDefinition**

- Standard form with labeled inputs
- Pipe-delimited fields (e.g., `classification_ids`) get an "Add X" button that adds a new input row
- Pre-filled if session data exists

### Table-based multi-entry forms
**Organization, Substance, Ingredient, RegulatedAuthorization**

- Editable data table with "+" button to add rows
- Trash icon to remove rows
- Organization: type selector (MAH, MRA, etc.) drives prefix in FSH
- Ingredient: role selector (active/excipient) drives validation rules

### Card-based multi-entry forms
**ClinicalUseDefinition, Composition**

- Cards with expand/collapse
- ClinicalUse: type selector (indication/contraindication/interaction) toggles relevant fields
- Composition: 8 rich-text fields for leaflet sections (use contenteditable divs or textareas)

### Table with sub-rows
**PackagedProductDefinition**

- Table-based but packing layers (type, quantity, material) are a nested sub-table per row

### Simple form
**Bundle** — identifier + language + "Generate" button

## 6. Validation

### Client-side (Alpine.js, no server roundtrip)
- Required fields marked with `*`
- No spaces in identifiers: `x-model` with regex reject
- Numeric fields: `type="number" step="any"`
- No newlines in single-line fields
- Max length warnings for FHIR-limited fields

### Server-side (validator.py, on POST)
- Reuse existing validators: `if_has_spaces`, `if_numeric_or_null`, `if_numeric`, `if_has_newline`
- Added: cross-field consistency (e.g., Ingredient `role=active` requires `StrengthBasis`)
- Added: reference integrity (e.g., at least one MAH Organization exists)

### Pre-generation (on "Generate")
- All 11 sheets have data
- Singletons have exactly 1 row
- Cross-resource references resolve (Ingredient → Organization, etc.)

### Error display
- htmx returns the form partial with error messages injected inline
- Error state does NOT clear the user's input (preserved from POST body)
- Alpine.js adds instant visual feedback (red border, error text)

## 7. Lookup Data Service (`lookup.py`)

Load `EXTRA` and `DATA_VAL` sheets at startup into module-level dicts:

```python
LOOKUPS = {
    "dose_forms": [...],
    "routes": [...],
    "countries": [...],
    "languages": [...],
    "substances": [...],
    "org_types": [...],
    "packaging_types": [...],
    "packaging_materials": [...],
}
```

**Endpoints:**
- `GET /gh-epi-creator/api/lookup/<category>` — full list as JSON
- `GET /gh-epi-creator/api/lookup/<category>?q=term` — filtered list

**DATA_VAL cascading:** Selecting `unit_presentation` filters available `doseForms`; selecting `doseForm` filters available `routes`. Handled via Alpine.js fetching the relevant endpoint.

**Alpine.js autocomplete component:** Reusable `x-data="autocomplete"` pattern. Fetches from lookup API, shows dropdown, fills hidden input with selected ID while displaying label.

## 8. Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/gh-epi-creator/` | GET | Landing page with "Start" button |
| `/gh-epi-creator/wizard/new` | POST | Creates session, redirects to step 1 |
| `/gh-epi-creator/wizard/<step>` | GET | Renders form for step |
| `/gh-epi-creator/wizard/<step>` | POST | Validates + saves + redirects to next |
| `/gh-epi-creator/wizard/<step>/prev` | GET | Go back one step |
| `/gh-epi-creator/wizard/generate` | POST | Runs FSH generation, returns download URL |
| `/gh-epi-creator/wizard/download` | GET | Serves generated zip |
| `/gh-epi-creator/api/lookup/<category>` | GET | JSON lookup data |
| `/gh-epi-creator/faq` | GET | FAQ (unchanged) |

## 9. Generation Flow (revised)

```
session["data"] dict
       |
       v
  functions.create_from_session(session_data)
       |-- Builds pandas DataFrames from session dict (in memory)
       |-- Adds UUID id_hash column
       |-- PASS 1: Jinja2 renders FSH from DataFrames → writes .fsh files
       |-- Scans .fsh files, extracts Instance IDs → reference map
       |-- PASS 2: Re-renders .fsh with cross-references
       v
  subprocess.run(["sushi", "."])
       v
  Copy Bundle JSON to output/
       v
  Zip results → download URL
```

## 10. Removed Functionality

- Excel upload route and UI
- `acmeDrug.xlsx` template download
- `pd.read_excel()` calls
- CSV intermediate files (temp/*.csv)
- The `pre_validation()` comment/uncomment pattern — validation is now always active

## 11. Implementation Order

1. Refactor `functions.py`: extract `create_from_session()` that takes a dict, builds DataFrames, runs two-pass render
2. Build `lookup.py`: load EXTRA/DATA_VAL, serve JSON endpoints
3. Build `validator.py` reactivation + new rules
4. Build wizard base template + sidebar partial
5. Build forms (11 templates + htmx routes) in step order
6. Wire up Alpine.js autocomplete + client-side validation
7. Update landing page (remove upload, add "Start" button)
8. Integration test: full flow from form → generate → download
9. Cleanup: remove Excel-related code and files
