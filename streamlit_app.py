#!/usr/bin/env python
# coding: utf-8

import streamlit as st
from os import listdir, getcwd, mkdir, system, remove
from os.path import exists
from jinja2 import Environment, FileSystemLoader, Template
import pandas as pd
import uuid
import re
from datetime import datetime
import shutil
import subprocess
from functions import create_from_template, create_env
from zipfile import ZipFile


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

        result = subprocess.run(["sushi", "."], stdout=subprocess.PIPE)
        # system("sushi .")
        f = open(download_folder + "/" + "result.txt", "w")
        f.write(result.stdout.decode("utf-8"))
        f.close()

        # result.stdout
        for json_file in listdir("fsh-generated/resources"):
            if json_file.startswith("Bundle"):
                shutil.move("fsh-generated/resources/" + json_file, zip_folder)

        # ...

        zip_file_name = major_name + "_results.zip"
        # remove(zip_file_name)
        myzipfile = ZipFile(zip_file_name, mode="a")
        print(listdir(zip_folder))
        # Add zip_folder to the zip file
        myzipfile.write(zip_folder, arcname="zip_folder")
        print(listdir(real_output_folder))

        # Add real_output_folder to the zip file
        myzipfile.write(real_output_folder, arcname="real_output_folder")
        print(listdir(download_folder))

        # Add download_folder to the zip file
        myzipfile.write(download_folder + "/" + "result.txt", arcname="result.txt")
        myzipfile.close()

        col3, col4 = st.columns(2)

    with open(zip_file_name, "rb") as fp:
        btn = col3.download_button(
            label="Download ZIP with results",
            data=fp,
            file_name=zip_file_name,
            mime="application/zip",
        )
