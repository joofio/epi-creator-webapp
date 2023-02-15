
Instance: bundlepackageleaflet-humira
InstanceOf: BundleUvEpi
Title: "ePI document Bundle for humira Package Leaflet"
Description: "Bundle for humira Package Leaflet ePI document"
Usage: #example

* id = "6739a04d-e70a-40c7-aa72-544b39a5df39" 
* identifier.system = "https://www.gravitatehealth.eu/sid/doc" 
* identifier.value = "nan"
* type = #document
* timestamp = "2023-02-15T21:06:31Z"

// Composition
* entry[0].fullUrl = "Composition/ac797604-94f7-4062-a5de-8b1478096b3e"
* entry[0].resource = compositionhumira

 
 
 

 
 

// Ingredient

* entry[+].fullUrl = "Ingredient/4245b64c-3649-4c10-9d57-ace91dda8cc7"
* entry[=].resource = ingredient-for-acme-mannitol 

// Ingredient

* entry[+].fullUrl = "Ingredient/f16dbbc7-37a6-46e1-9f1b-e910ba5c3ea3"
* entry[=].resource = ingredient-for-acme-polysorbate80 

// Ingredient

* entry[+].fullUrl = "Ingredient/6820b5a5-48de-4ec2-b311-ac2a6b871552"
* entry[=].resource = ingredient-for-acme-adalimumab 

// Ingredient

* entry[+].fullUrl = "Ingredient/e5a802b1-0506-42b5-8c9a-4659a5b192d1"
* entry[=].resource = ingredient-for-acme-sterilewaterforinjection 

// Ingredient

* entry[+].fullUrl = "Ingredient/a790667e-4719-4f3e-acda-69053a5375cb"
* entry[=].resource = ingredient-for-acme-citricacidmonohydrate 

// Ingredient

* entry[+].fullUrl = "Ingredient/6931238e-7076-4006-aa14-c1e9ca0374ef"
* entry[=].resource = ingredient-for-acme-sodiumcitrateunspecifiedform 

// Ingredient

* entry[+].fullUrl = "Ingredient/8a3752f9-6b2d-4028-8a5f-fe0698d6d8d0"
* entry[=].resource = ingredient-for-acme-sodiumphosphatemonobasicdihydrate 

// Ingredient

* entry[+].fullUrl = "Ingredient/2321e835-b61f-4836-898d-1c1902332381"
* entry[=].resource = ingredient-for-acme-sodiumphosphatedibasicdihydrate 

// Ingredient

* entry[+].fullUrl = "Ingredient/7166c985-6b2d-4018-823b-781914ccad63"
* entry[=].resource = ingredient-for-acme-sodiumchloride 
 

// Substance
   
* entry[+].fullUrl = "SubstanceDefinition/eabdc045-1c55-49ac-8487-6a0b4862ed3e"
* entry[=].resource = substance-adalimumab 
 

// AdministrableProductDefinition

* entry[+].fullUrl = "AdministrableProductDefinition/a414f849-30e7-46c3-b757-02d21d66fa6d"
* entry[=].resource = ap-humira40mgsolutionforinjectionsubcutaneoususeprefilledsyringeglass 
 

// RegulatedAuthorization

* entry[+].fullUrl = "RegulatedAuthorization/525991cf-64c7-440b-8af7-2b627026e3aa"
* entry[=].resource = authorizationhumira40mgsolutionforinjectioninprefilledsyringe 
 

// Organization

* entry[+].fullUrl = "Organization/dca60855-ac2f-4797-b424-7c5de9758041"
* entry[=].resource = org-marketingauthorisationholder-abbviedeutschlandgmbhcokg-acme 
 

// PackagedProductDefinition

* entry[+].fullUrl = "PackagedProductDefinition/dae76ab8-8c68-4176-b797-e5f52f3e8f9f"
* entry[=].resource = ppd-humira40mgsolutionforinjectioninprefilledsyringe2prefilledsyringes2alcoholpads 
 

// MedicinalProductDefinition

* entry[+].fullUrl = "MedicinalProductDefinition/ea5e812e-3dee-4aa3-9c99-034a63737c03"
* entry[=].resource = mpHumira40mgSolutionforinjectionSubcutaneoususeprefilledsyringeglass 
 

// ManufacturedItemDefinition

* entry[+].fullUrl = "ManufacturedItemDefinition/c20c2604-9d28-4ad9-aa99-a5fc94301f6f"
* entry[=].resource = mid-humira40mgsolutionforinjectionsubcutaneoususeprefilledsyringeglass 
 

