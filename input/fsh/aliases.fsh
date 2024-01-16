//============== ALIAS ===============

// =========== Code Systems =======
Alias: $uri = urn:ietf:rfc:3986
Alias: $oid = urn:ietf:rfc:1155
Alias: $loinc = http://loinc.org
Alias: $iso3166 = urn:iso:std:iso:3166
Alias: $sct = http://snomed.info/sct
Alias: $phenxtoolkit = https://www.phenxtoolkit.org
Alias: $observation-category = http://terminology.hl7.org/CodeSystem/observation-category
Alias: $location-physical-type = http://terminology.hl7.org/CodeSystem/location-physical-type
Alias: $consentscope = http://terminology.hl7.org/CodeSystem/consentscope
Alias: $atc = http://www.whocc.no/atc
Alias: $allergyintolerance-clinical = http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical
Alias: $allergyintolerance-verification = http://terminology.hl7.org/CodeSystem/allergyintolerance-verification
Alias: $condition-clinical = http://terminology.hl7.org/CodeSystem/condition-clinical
Alias: $list-order  = http://terminology.hl7.org/CodeSystem/list-order 
Alias: $spor-productNamePartType-cs = https://spor.ema.europa.eu/lists/220000000000 // Medicinal Product Name Part Type
Alias: $meddra = http://terminology.hl7.org/CodeSystem/mdr
Alias: $snomed = http://snomed.info/sct

Alias: $edqm = http://standardterms.edqm.eu

// --- Substances
Alias: $unii = http://fdasis.nlm.nih.gov
Alias: $ginas = https://gsrs.ncats.nih.gov/ginas/app/beta
Alias: $spor-sms = https://spor.ema.europa.eu/smswi  // Invented, to be checked

Alias: $ucum = http://unitsofmeasure.org
Alias: $fake-man-sys = https://www.gravitatehealth.eu/sid/man
Alias: $phpid = https://www.who-umc.org/phpid
Alias: $gs1 = https://www.gs1.org/gtin
Alias: $publication-status = http://hl7.org/fhir/publication-status
Alias: $composition-attestation-mode = http://hl7.org/fhir/composition-attestation-mode



Alias: $medicinal-product-name-part-type = http://hl7.org/fhir/medicinal-product-name-part-type
Alias: $medicationknowledge-characteristic = http://terminology.hl7.org/CodeSystem/medicationknowledge-characteristic


Alias: $spor-prod = https://spor.ema.europa.eu/pmswi // invented to be updated
Alias: $spor = https://spor.ema.europa.eu
Alias: $spor-org = https://spor.ema.europa.eu/omswi

Alias: $spor-rms = https://spor.ema.europa.eu/rmswi
Alias: $spor-man = http://ema.europa.eu/fhir/marketingAuthorizationNumber

//  VALUE SETS

Alias: $VS-composition-status =	http://hl7.org/fhir/ValueSet/composition-status
Alias: $VS-publication-status = http://hl7.org/fhir/ValueSet/publication-status

Alias: $VS-medicinal-product-type =
	http://hl7.org/fhir/ValueSet/medicinal-product-type
	
Alias: $VS-medicinal-product-domain =
	http://hl7.org/fhir/ValueSet/medicinal-product-domain
	
	


// =========== Extensions =======
Alias: $event-location = http://hl7.org/fhir/StructureDefinition/event-location
Alias: $data-absent-reason = http://hl7.org/fhir/StructureDefinition/data-absent-reason


// =========== Profiles =======

Alias: $MedicationStatement-uv-ips = http://hl7.org/fhir/uv/ips/StructureDefinition/MedicationStatement-uv-ips
Alias: $Patient-uv-ips = http://hl7.org/fhir/uv/ips/StructureDefinition/Patient-uv-ips
Alias: $Practitioner-uv-ips = http://hl7.org/fhir/uv/ips/StructureDefinition/Practitioner-uv-ips
Alias: $Condition-uv-ips = http://hl7.org/fhir/uv/ips/StructureDefinition/Condition-uv-ips
Alias: $clinicaldocument = http://hl7.org/fhir/StructureDefinition/clinicaldocument



// Define a local code system
CodeSystem: QuestionnaireDimensionCS
Id:         questi-dimens-cs
Title:     "Questionnaire example Dimensions"
Description:  "Questionnaire example Dimensions"
* ^experimental = true
* ^caseSensitive = true


//* ^url = http://hl7.eu/fhir/ig/gravitate-health/CodeSystem/questi-dimens-cs
* #None
    "None"
    "None"
* #F
    "Female"
    "Female"
* #M
    "Male"
    "Male"

* #O
    "Other Gender"
    "Other Gender"
* #ND
    "Non-disclosed Gender"
    "Non-disclosed Gender"
    
* #0
    "Non Smoker"

* #1
    "1-5"

* #2
    "6-20"

* #3
    ">20"

* #SINGLE
    "single"

* #SOME
    "Some"

* #SOME23
    "Some (2-3)"
* #MANY
    "Many"

* #Low
    "Low"
    "Low"

* #Medium
    "Medium"
    "Medium"


* #High
    "High"
    "High"

* #U
    "Unemployed/Retired"

* #EM
    "Employed Manual"

* #ENM
    "Employed non Manual"


ValueSet: ThreepointCategoryVS
Id:         3point-category-vs

* questi-dimens-cs#Low
* questi-dimens-cs#Medium
* questi-dimens-cs#High


// Define a local code system
CodeSystem: PDcategoryCS
Id:         pd-category-cs
Title:     "Persona Vector Dimensions categories"
Description:  "Persona Vector Dimensions categories"
* ^experimental = true
* ^caseSensitive = true
//* ^url = http://hl7.eu/fhir/ig/gravitate-health/CodeSystem/pd-category-cs


ValueSet: PDcategoryVS

// for category

// Define a local code system
CodeSystem: PDtypeCS
Id:         pd-type-cs
Title:     "Persona Vector Dimensions Code"
Description:  "Persona Vector Dimensions Code"
//* ^url = http://hl7.eu/fhir/ig/gravitate-health/CodeSystem/pd-type-cs
* ^experimental = true
* ^caseSensitive = true

* #EMP
    "employment"


* #SHW
    "Share info Willingly"

* #WKL
    "WorkLife"

* #ER
    "Emotional/Rational"

* #EVI
    "Extrovert/introvert"

* #DL
    "Digital Literacy"


* #HL
    "Health Literacy"

* #TSI
    "Tool Support Interest"


ValueSet: PDtypeVS
// for type
* include codes from system http://hl7.eu/fhir/ig/gravitate-health/CodeSystem/pd-type-cs



// Define a local code system
CodeSystem: EpicategoryCS
Id:         epicategory-cs
Title:     "Category of EPI"
Description: "Category of EPI"
* ^experimental = true
* ^caseSensitive = true


//* ^url = http://hl7.eu/fhir/ig/gravitate-health/CodeSystem/epicategory-cs
* #R
    "Raw"
    "Raw"
* #F
    "Focused"
    "Focused"
* #P
    "Processed"
    "Processed"

// Define a local code system
CodeSystem: ICPC2CS
Id:         icpc-2-cs
Title:     "Example ICPC2 CS"
Description: "Example ICPC2 CS"
* ^experimental = true
* ^caseSensitive = true

//* ^url =  http://gravitate.eu/CodeSystem/icpc-2
// Spacing layout over three lines per term is optional, for clarity
// The definition (second text string) is optional
* #B90
    "HIV-infection/AIDS"
    "HIV-infection/AIDS"
* #R80
    "Influenza"
    "Influenza"
* #R81
    "Pneumonia"
    "Pneumonia"
* #P74
    "Anxiety disorder/anxiety state"
    "Anxiety disorder/anxiety state"
* #W78
    "Pregnancy"
    "Pregnancy"

* #W27
    "Fear of complications of pregnancy"
    "Fear of complications of pregnancy"
* #D07
    "Dyspepsia/indigestion"
    "Dyspepsia/indigestion"
* #A84
    "Poisoning by medical agent"
    "Poisoning by medical agent"
* #P19
    "Drug abuse"
    "Drug abuse"
* #P18
    "Medication abuse"
    "Medication abuse"
* #B99
    "Blood/lymph/spleen disease other"
    "Blood/lymph/spleen disease other"
* #D97
    "Liver disease NOS"
    "Liver disease NOS"

* #A13
    "Concern/fear medical treatment"
    "Concern/fear medical treatment"

* #A78
    "Infectious disease other/NOS "
    "Infectious disease other/NOS "

* #P03
    "Feeling depressed"
    "Feeling depressed"

* #U72
    "Urethritis"
    "Urethritis"

* #K86
    "Hypertension uncomplicated"
    "Hypertension uncomplicated"

* #T89
    "Diabetes insulin dependent"
    "Diabetes insulin dependent"
* #T90
    "Diabetes non-insulin dependent"
    "Diabetes non-insulin dependent"
* #K22
    "Risk factor cardiovascular disease"
    "Risk factor cardiovascular disease"
* #D93
    "Irritable bowel syndrome"
    "Irritable bowel syndrome"
