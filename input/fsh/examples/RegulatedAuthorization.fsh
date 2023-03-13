
Instance: authorizationhipricoarkopharmacpsulasduras
InstanceOf: RegulatedAuthorizationUvEpi
Title: "Regulated Authorization for HIPÉRICO ARKOPHARMA cápsulas duras"
Description: "Regulated Authorization for HIPÉRICO ARKOPHARMA cápsulas duras"
Usage: #example


* id = "bd75538b-b198-420b-a99f-9c2d04f7d2a3" 

* identifier.system = $spor-prod
* identifier.value = "79963"
* identifier.use = #official

 // Reference to MedicinalProductDefinition: EU/1/97/049/001 Karvea 75 mg tablet
 //* subject = Reference(karvea75mgblisterx28)
* subject = Reference(mpHIPRICOARKOPHARMAcpsulasduras)
* type = $spor-rms#100000072062 "Marketing Authorisation"

//* type = $spor-rms#100000072062
//* type.text = "Marketing Authorisation"

* region = urn:iso:std:iso:3166#ES "Spain"


* status = http://hl7.org/fhir/publication-status#active "Active"


* statusDate = "2015-01-01"
// * holder = Reference(sanofiaventisgroupe)
 


* holder = Reference(org-marketingauthorisationholder-arkopharmalaboratoriossau-acme)


 

