#!/usr/bin/env python
# coding: utf-8

import streamlit as st
from os import listdir, getcwd, mkdir, rmdir
from os.path import isfile, join, exists
import glob
from jinja2 import Template, Environment, FileSystemLoader

import pandas as pd
from pathlib import Path
import numpy as np
import sys
import uuid
import re
from datetime import datetime
from jinja2 import Template, Environment, FileSystemLoader
import pandas as pd
from pathlib import Path
import sys
import uuid
import re
from datetime import datetime
import shutil


context = {"now": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")}

st.set_option("deprecation.showPyplotGlobalUse", False)


st.markdown("""Please upload the excel file for creating the FSH resources.""")

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

major_name = st.text_input("Product Name", "acme").replace(" ", "_")

uploaded_file = st.file_uploader("Choose a file")

# Custom filter method
def regex_replace(s, find, replace):
    """A non-optimal implementation of a regex filter"""
    return re.sub(find, replace, s)


env = Environment(loader=FileSystemLoader("./templates/"), trim_blocks=True)
env.filters["regex_replace"] = regex_replace

# print(getcwd())
temp_folder = getcwd() + "/temp/"
if not exists(temp_folder):
    mkdir(temp_folder)

real_output_folder = getcwd() + "/output/"
if not exists(real_output_folder):
    mkdir(real_output_folder)


if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # st.write(bytes_data)

    df1 = pd.read_excel(uploaded_file)

    for sheet in elements:
        # read an excel file and convert
        # into a dataframe object
        df = pd.DataFrame(pd.read_excel(uploaded_file, sheet_name=sheet))
        df["id_hash"] = df["id"].apply(lambda x: uuid.uuid4())
        df["id"].fillna(df["id_hash"], inplace=True)

        df.to_csv(temp_folder + sheet + ".csv", index=True)

    data_dict = {"MajorName": major_name}  # if needed
    data = {"dictionary": data_dict, "turn": "1"}
    print("temp")
    print(listdir(temp_folder))
    print("real outpu")
    print(listdir(real_output_folder))
    print("templates")
    print(listdir("templates/"))

    for file in listdir(temp_folder):
        print(file)
        n_file = file.split(".")[0]
        # with open(TEMPLATE_FOLDER + n_file + ".fsh", "r") as file:

        # templateString = env.get_template(file.read())

        t = env.get_template(n_file + ".fsh")
        # t = Template(templateString, trim_blocks=True)

        df = pd.read_csv(temp_folder + n_file + ".csv", index_col=0)

        df = df.astype(str)
        data["data"] = df
        t.stream(data=data, **context).dump(real_output_folder + n_file + ".fsh")

        # get ids:
        ## goes for all, checks for ID and adds to list
        ## then creates again with references
    object_ids = {}
    for file in listdir(real_output_folder):
        #  print(file)
        # n_file = file.split(".")[0]
        with open(real_output_folder + file, "r") as file1:
            Lines = file1.readlines()
            instances = []
            ids = []
            for line in Lines:

                if "Instance: " in line:
                    # print(line)
                    instances.append(line.replace("Instance: ", "").strip())
                if "* id = " in line:
                    # print(line)
                    ids.append(line.replace("* id = ", "").replace('"', "").strip())

            object_ids[file.split(".")[0]] = [(i, j) for i, j in zip(instances, ids)]

    print(object_ids)
    data["references"] = object_ids

    print("newline" + " ---" * 30)
    # multiple elementsa
    for file in listdir(temp_folder):
        # print(file)
        n_file = file.split(".")[0]
        # with open(TEMPLATE_FOLDER + n_file + ".fsh", "r") as f:
        #     templateString = f.read()
        # t = Template(templateString, trim_blocks=True)
        t = env.get_template(n_file + ".fsh")

        df = pd.read_csv(temp_folder + file, index_col=0)
        # print(df)
        df = df.astype(str)
        data["data"] = df
        data["turn"] = "2"
        t.stream(data=data, **context).dump(real_output_folder + n_file + ".fsh")

    # zip folder
    # csv = convert_df(my_large_df)
    zipfile = shutil.make_archive(major_name, "zip", real_output_folder)

    print(listdir("."))
    with open(zipfile, "rb") as fp:
        btn = st.download_button(
            label="Download ZIP",
            data=fp,
            file_name=major_name + ".zip",
            mime="application/zip",
        )
