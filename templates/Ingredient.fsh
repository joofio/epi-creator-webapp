{% for index,row in data["data"].iterrows() %}
{% if row["skip"] not in ['y', 'Y', 'x', 'X'] %}

{% set ns = namespace() %}
{% set ns.one = data["dictionary"]["MajorName"]|lower|regex_replace('[^A-Za-z0-9]+', '') %}
{% set ns.two = row["name"]| lower | regex_replace('[^A-Za-z0-9]+', '')  %}
{% set ns.name_to_has= ns.one ~ ns.two  %}

{% if ns.name_to_has|length > 48 %}
Instance: ingredient-for-{{ns.name_to_has| create_hash_id}}
{% else %}
Instance: ingredient-for-{{ data["dictionary"]["MajorName"]|lower|regex_replace('[^A-Za-z0-9]+', '')}}-{{ row["name"]| lower | regex_replace('[^A-Za-z0-9]+', '') }}
{% endif %}

InstanceOf: IngredientUvEpi
Title: "Ingredient-{{row["role"]| lower}} {{ row["name"]  }}"
Description: "{{ row["name"]  }}"
Usage: #example

* identifier.system = $ginas
* identifier.value = "{{ row["identifier"]|trim  }}"
* identifier.use = #official

* role = $spor-rms#{{ row["roleID"]  }} "{{ row["role"]  }}"

* status = #active

{% if row["identifier"]|string not in ("nan","") %}
{% set _sub_key = data["substance_lookup"].get(row["identifier"]|trim) if data.get("substance_lookup") else None %}
* substance.code.concept.coding = $ginas#{{ row["identifier"]|trim }} "{{ row["name"] | trim  }}"
{% if _sub_key %}
* substance.code = Reference(substance-{{ _sub_key }})
{% else %}
// ERROR[2] - No Substance found with identifier "{{ row["identifier"]|trim }}"; cannot emit substance.code Reference. INDEX:{{ index + 1 }}
{% endif %}
{% else %}
// ERROR[1] - Ingredient identifier (substance code) is empty; cannot emit substance.code. INDEX:{{ index + 1 }}
{% endif %}

{% if row["StrengthBasis"]|string not in ("nan","") %}
{% if row["quantity"]|string not in ("nan","") %}

* substance.strength.presentationQuantity = {{ row["quantity"] | replace (",",".")|int  }} '{{ row["quantity unit"]  }}'
{% endif %}

* substance.strength.basis = http://terminology.hl7.org/CodeSystem/v3-RoleClass#{{row["StrengthBasis"]}} "{{row["StrengthBasisText"]|trim }}"
{% endif %}


{% if data["turn"] != "1" %}
// Reference to products
* for = Reference({{data["references"]["ManufacturedItemDefinition"][0][0]}})
* for[+] = Reference({{data["references"]["MedicinalProductDefinition"][0][0]}})
* for[+] = Reference({{data["references"]["AdministrableProductDefinition"][0][0]}})

{%- endif %}

{% set ns  = namespace(referenced=False) -%}
{% if data["turn"] != "1" %}
{% for refs in data["references"]["Organization"] %} 
{% if refs[0].startswith("mapi") %}
{% set ns.referenced=True -%}

* manufacturer.manufacturer  = Reference({{refs[0]}})
{%- endif %}
{%- endfor %}

{% if not ns.referenced  %}

//* manufacturer.manufacturer = Reference({{data["references"]["Organization"][0][0]}})
{% endif %}
{% endif %}
{% endif %}
{% endfor %}