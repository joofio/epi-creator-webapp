
Instance: ap-hipricoarkopharmacpsulasduras
InstanceOf: AdministrableProductDefinitionUvEpi
Title: "Administrable product HIPÉRICO ARKOPHARMA cápsulas duras"
Description: "HIPÉRICO ARKOPHARMA cápsulas duras"
Usage: #example

* id = "5be31d26-9639-4056-b88f-a0f6b148cc0c" 
* identifier.system = $phpid
* identifier.value = "xx" 

* status = #active

* formOf = Reference(mpHIPRICOARKOPHARMAcpsulasduras)
* administrableDoseForm = $spor-rms#100000073681 "Hard capsules"
* unitOfPresentation = $spor-rms#200000002152 "hard capsule"

//this is just manufactured with extra steps?


//reference to MedicinalProductDefinition: EU/1/97/049/001 Karvea 75 mg tablet
* producedFrom = Reference(mid-hipricoarkopharmacpsulasduras)


* routeOfAdministration.code = $spor-rms#100000073619 "Oral use"

* routeOfAdministration.targetSpecies.code = $spor-rms#100000109093 "Human"