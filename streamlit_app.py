#!/usr/bin/env python
# coding: utf-8

import streamlit as st
from os import listdir, getcwd, mkdir, system
from os.path import exists
from jinja2 import Environment, FileSystemLoader, Template
import pandas as pd
import uuid
import re
from datetime import datetime
import shutil
import subprocess
from functions import create_from_template, create_env

context = {"now": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")}

st.set_option("deprecation.showPyplotGlobalUse", False)

st.header("""ePI Creator""")

st.markdown(
    """Please upload the excel file for creating the FSH resources.
    Name the file the product that you are creating.   
    If you want to check the FHIR profiles, see [here](http://build.fhir.org/ig/HL7/emedicinal-product-info/artifacts.html).  
    If you want to check examples, see [here](http://build.fhir.org/ig/hl7-eu/gravitate-health/).

    """
)

elements = [
    "AdministrableProductDefinition",
    "Substance",
    "RegulatedAuthorization",
    "Organization",
    "ClinicalUseDefinition",
    "Composition",
    "Ingredient",
    "MedicinalProductDefinition",
    "ManufacturedItemDefinition",
    "PackagedProductDefinition",
    "Bundle",
]
col1, _ = st.columns(2)

fp = open("acmeDrug.xlsx", "rb")

col1.download_button(
    label="Download example excel",
    data=fp,
    file_name="acmeDrug.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

uploaded_file = st.file_uploader("Choose a file")

# print(getcwd())
temp_folder = getcwd() + "/temp/"
if not exists(temp_folder):
    mkdir(temp_folder)

zip_folder = getcwd() + "/output/"
if exists(zip_folder):
    shutil.rmtree(zip_folder)
mkdir(zip_folder)

real_output_folder = "input/fsh/examples/"
if not exists(real_output_folder):
    mkdir(real_output_folder)
download_folder = "downloads/"
if not exists(download_folder):
    mkdir(download_folder)

templates_folder = "templates/"

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # st.write(bytes_data)
    major_name = uploaded_file.name.replace(" ", "_").replace(".xlsx", "")
    env = create_env(templates_folder)
    with st.spinner("Processing..."):

        create_from_template(
            env,
            uploaded_file,
            templates_folder,
            real_output_folder,
            major_name=major_name,
        )
        # zip folder
        # csv = convert_df(my_large_df)
        zipfile = shutil.make_archive(
            download_folder + "/" + major_name + "fsh", "zip", real_output_folder
        )
        result = subprocess.run(["sushi", "."], stdout=subprocess.PIPE)
        # system("sushi .")
        f = open(download_folder + "/" + "result.txt", "w")
        f.write(result.stdout.decode("utf-8"))
        f.close()

        # result.stdout
        for json_file in listdir("fsh-generated/resources"):
            if json_file.startswith("Bundle"):
                shutil.move("fsh-generated/resources/" + json_file, zip_folder)
        zipfile2 = shutil.make_archive(
            download_folder + "/" + major_name + "json", "zip", zip_folder
        )

        # print(listdir("."))
        col3, col4, col5 = st.columns(3)

    with open(zipfile, "rb") as fp:
        btn = col3.download_button(
            label="Download ZIP with FSH files",
            data=fp,
            file_name=download_folder + "/" + major_name + "_fsh.zip",
            mime="application/zip",
        )

    with open(zipfile2, "rb") as fp2:
        btn2 = col4.download_button(
            label="Download ZIP with JSON files",
            data=fp2,
            file_name=download_folder + "/" + major_name + "_json.zip",
            mime="application/zip",
        )
    with open(download_folder + "/" + "result.txt", "rb") as fp3:
        btn2 = col5.download_button(
            label="Download Log file",
            data=fp3,
            file_name="log.txt",
        )
