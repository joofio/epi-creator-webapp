{% for index,row in data["data"].iterrows() %}
{% if row["skip"] not in ['y', 'Y', 'x', 'X'] %}

{% set ns = namespace() %}
{% set ns.one = row['type'] %}
{% set ns.two = row['name'] %}
{% set ns.three= data["dictionary"]["MajorName"] %}
{% set ns.name_to_has= ns.one ~ ns.two ~ns.three  %}

//{{row["type"]}}
{% if row["type"]| lower == "marketing authorisation holder" %}
{% set ns.org_type= "mah" %}
{% elif row["type"]|lower == "medicines regulatory authority" %}
{% set ns.org_type= "mra" %}
{% elif row["type"]|lower == "manufacturer" %}
{% set ns.org_type= "man" %}
{% elif row["type"]|lower == "master file holder" %}
{% set ns.org_type= "mfh" %}
{% elif row["type"]|lower == "contact location" %}
{% set ns.org_type= "cl" %}
{% elif row["type"]|lower == "manufacturer batch release" %}
{% set ns.org_type= "mbr" %}
{% elif row["type"]|lower == "manufacturer api" %}
{% set ns.org_type= "mapi" %}
{% else %}
{{ "// ERROR[11] - Not a format for type  INDEX:{}".format(index+1)  }}
{% set ns.org_type= "org" %}
{% endif %}




Instance: {{ns.org_type}}-{{ns.name_to_has| create_hash_id}}

InstanceOf: OrganizationUvEpi
Title: "{{ row["name"]  }} as {{ row["type"]  }}"
Description: "{{ row["name"]  }} as {{ row["type"]  }}"
Usage: #example

{% if row["identifier"]|string not in ("nan","") -%}
* identifier.system = $spor-org
* identifier.value = "{{ row["identifier"]|trim }}"
* identifier.use = #official
{%- endif %}

* active = true 
{% if ns.org_type== "mapi" or ns.org_type== "mbr" -%}
* type = $spor-rms#220000000033  "Manufacturer"

{% else %}
* type = $spor-rms#{{row["typeID"]}}  "{{ row["type"]  }}"
{% endif %}
//* type.text = "{{ row["type"]  }}"
* name = "{{ row["name"]  }}"


* contact
  * address
    {{ "* text = \"{} {} {}\"".format(row.address_line|trim,row.address_city|trim|replace('nan',''),row.address_countryName|trim|replace('nan','')) }}
    * use = #work
    * type = #physical
    {{ "* line = \"{}\"".format(row.address_line|trim) if row.address_line|string not in ("nan","")}}
    {{ "* city = \"{}\"".format(row.address_city|trim) if row.address_city|string not in ("nan","")}}
    {% if row.address_country|string not in ("nan","") and row.address_country|trim %}
    {% set ns.country_alpha3 = row.address_country|iso2to3 %}
    {% if ns.country_alpha3 %}
    {% if row.address_countryName|string not in ("nan","") and row.address_countryName|trim %}
    * country = "{{ ns.country_alpha3 }}" "{{ row.address_countryName|trim }}"
    {%- else %}
    * country = "{{ ns.country_alpha3 }}"
    {%- endif %}
    {% else %}
    // WARNING[org-country] - no alpha-3 mapping for address_country='{{ row.address_country|trim }}' in INDEX:{{ index+1 }}
    {%- endif %}
    {%- endif %}
    {{ "* postalCode = \"{}\"".format(row.address_postalCode|trim) if row.address_postalCode|string not in ("nan","")}}


{%- endif %}
{%- endfor %}