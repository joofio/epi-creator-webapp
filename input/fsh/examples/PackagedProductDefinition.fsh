
Instance: ppd-hipricoarkopharmacpsulasduras
InstanceOf: PackagedProductDefinitionUvEpi
Title: "HIPÉRICO ARKOPHARMA cápsulas duras"
Description: "HIPÉRICO ARKOPHARMA cápsulas duras"
Usage: #example
* id = "53df4e8e-543c-47f8-9cac-3afdf4c753d5" 

* identifier.system = $spor-prod
* identifier.value = "x"
* identifier.use = #official

* name = "HIPÉRICO ARKOPHARMA cápsulas duras"

* type = $spor-rms#100000155527 "Chemical Medicinal Prodcut"
//* type = $spor-rms#100000155527


* status = http://hl7.org/fhir/publication-status#active "Active"
* statusDate = "2015-01-03"


* containedItemQuantity =  '175'


* copackagedIndicator = false


* packaging
  * identifier.system = $spor-prod
  * identifier.value = "123456"
  * type = $spor-rms#100000073496 "Blister"
  * quantity = 30
  * material = $spor-rms#xxx "cardboard"



//reference to MedicinalProductDefinition: EU/1/97/049/001 Karvea 75 mg tablet
* packageFor = Reference(mpHIPRICOARKOPHARMAcpsulasduras)
 // Reference to Organization: MAH
* manufacturer = Reference(org-marketingauthorisationholder-arkopharmalaboratoriossau-acme)
