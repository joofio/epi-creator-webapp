from os import listdir, getcwd, mkdir, path, walk, makedirs
from os.path import exists
from jinja2 import Environment, FileSystemLoader, Template
import pandas as pd
import uuid
import re
from datetime import datetime
from epi_creator.validator import pre_validation
import hashlib
from html import unescape
import shutil
import subprocess
from zipfile import ZipFile

context = {"now": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")}
CANONICAL_URL = "http://hl7.eu/fhir/ig/gravitate-health/"


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


def add_folder_to_zip(zipfile, folder_path, arcname):
    for root, dirs, files in walk(folder_path):
        for file in files:
            filepath = path.join(root, file)
            zipfile.write(
                filepath,
                arcname=path.join(arcname, path.relpath(filepath, folder_path)),
            )


def process_file(uploaded_file):
    print(uploaded_file)
    temp_folder = getcwd() + "/temp/"
    print(temp_folder)
    if not exists(temp_folder):
        mkdir(temp_folder)

    zip_folder = getcwd() + "/output/"
    if exists(zip_folder):
        shutil.rmtree(zip_folder)
    mkdir(zip_folder)

    real_output_folder = getcwd() + "/input/fsh/examples/"
    print(real_output_folder)
    makedirs("input", exist_ok=True)
    makedirs("input/fsh", exist_ok=True)
    makedirs(real_output_folder, exist_ok=True)

    # if not exists(real_output_folder):
    #    mkdir(real_output_folder)
    download_folder = "downloads/"
    if not exists(download_folder):
        mkdir(download_folder)

    templates_folder = "templates/"

    major_name = uploaded_file.split("/")[-1].replace(" ", "_").replace(".xlsx", "")
    print(major_name)
    env = create_env(templates_folder)

    create_from_template(
        env,
        uploaded_file,
        templates_folder,
        real_output_folder,
        major_name=major_name,
    )
    # zip folder
    # csv = convert_df(my_large_df)

    result = subprocess.run(["npx","sushi", "."], stdout=subprocess.PIPE)
    # system("sushi .")
    f = open(download_folder + "/" + "result.txt", "w")
    f.write(result.stdout.decode("utf-8"))
    f.close()

    # result.stdout
    for json_file in listdir("fsh-generated/resources"):
        if json_file.startswith("Bundle"):
            shutil.move("fsh-generated/resources/" + json_file, zip_folder)

    zip_file_name = "epi_creator/" + major_name + "_results.zip"
    with ZipFile(zip_file_name, "w") as myzipfile:
        add_folder_to_zip(myzipfile, zip_folder, "json-files")
        add_folder_to_zip(myzipfile, real_output_folder, "fsh-files")
        add_folder_to_zip(myzipfile, download_folder, "result")

    return zip_file_name


def create_env(TEMPLATE_FOLDER):
    env = Environment(loader=FileSystemLoader(TEMPLATE_FOLDER), trim_blocks=True)

    # Custom filter method
    def regex_replace(s, find, replace):
        """A non-optimal implementation of a regex filter"""
        return re.sub(find, replace, s)

    env.filters["regex_replace"] = regex_replace

    def html_unescape(s):
        return (
            s.replace("&nbsp;", "")
            .replace("<br>", "")
            .replace("&oacute;", "ó")
            .replace("&aacute;", "á")
            .replace("&eacute;", "é")
            .replace("&iacute;", "í")
            .replace("&ntilde;", "ñ")
            .replace("&rsquo;", "'")
            .replace("&uacute;", "ú")
            .replace("&uuml;", "ü")
        )

    env.filters["html_unescape"] = html_unescape

    def hash_id(string):
        hash_object = hashlib.md5(bytes(string, "utf-8"))
        return str(hash_object.hexdigest())

    env.filters["create_hash_id"] = hash_id
    return env


def quality_checks(DATA_FILE, OUTPUT_FOLDER, major_name):
    if OUTPUT_FOLDER[-1] != "/":
        OUTPUT_FOLDER += "/"

    # writing to file

    for path in listdir(OUTPUT_FOLDER):
        print(path)
        file = open(OUTPUT_FOLDER + "/" + path, "r")
        # with open(file) as f:
        lines = file.readlines()
        for idx, line in enumerate(lines):
            if "None" in line:
                print("ISSUE on line: ", str(idx), "file ->", path)
                print(line)
            if '"nan"' in line:
                print("ANOTHER ISSUE on line: ", str(idx), "file ->", path)
                print(line)
            if ".0" in line:
                print("ANOTHER ISSUE on line: ", str(idx), "file ->", path)
                print(line)


def create_from_template(env, DATA_FILE, TEMPLATE_FOLDER, OUTPUT_FOLDER, major_name):
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

    # create temp_folder:
    print(DATA_FILE, TEMPLATE_FOLDER, OUTPUT_FOLDER)

    if TEMPLATE_FOLDER[-1] != "/":
        TEMPLATE_FOLDER += "/"
    if OUTPUT_FOLDER[-1] != "/":
        OUTPUT_FOLDER += "/"

    temp_folder = getcwd() + "/temp/"

    if not exists(temp_folder):
        mkdir(temp_folder)
    print(OUTPUT_FOLDER)
    if not exists(OUTPUT_FOLDER):
        mkdir(OUTPUT_FOLDER)
    for sheet in elements:
        # read an excel file and convert
        # into a dataframe object
        df = pd.DataFrame(pd.read_excel(DATA_FILE, sheet_name=sheet))
        #   pre_validation(df, sheet)
        df["id_hash"] = df["id"].apply(lambda x: uuid.uuid4())
        df["id"].fillna(df["id_hash"], inplace=True)
        # show the dataframe
        #   print(df)
        df.to_csv(temp_folder + sheet + ".csv", index=True)

    df = pd.read_csv(temp_folder + "MedicinalProductDefinition.csv", index_col=0)
    productname = df.loc[0, "productname"]
    data_dict = {
        "MajorName": major_name,
        "url": CANONICAL_URL,
        "productname": productname,
    }  # if needed
    data = {
        "dictionary": data_dict,
        "turn": "1",
    }

    # multiple elementsa
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
        t.stream(data=data, **context).dump(OUTPUT_FOLDER + n_file + ".fsh")

        # get ids:
        ## goes for all, checks for ID and adds to list
        ## then creates again with references
    object_ids = {}
    for file in listdir(OUTPUT_FOLDER):
        #  print(file)
        # n_file = file.split(".")[0]
        with open(OUTPUT_FOLDER + file, "r") as file1:
            Lines = file1.readlines()
            instances = []
            ids = []
            type_ = []
            # if file.split(".")[0] == "Organization":
            #     for line in Lines:
            #         if "Instance: " in line:
            #             instances.append(line.replace("Instance: ", "").strip())
            #         if "* type = $" in line:
            #             # print(line)
            #             type_.append(
            #                 line.split("  ")[-1].replace('"', "").replace('"\n', "")
            #             )
            #     object_ids[file.split(".")[0]] = {
            #         k: v for k, v in zip(type_, instances)
            #     }
            # else:
            for line in Lines:
                if "Instance: " in line:
                    instances.append(line.replace("Instance: ", "").strip())
                    # if "* id = " in line:
                    # print(line)
                    ids.append(line.replace("Instance: ", "").strip())

            object_ids[file.split(".")[0]] = [(i, j) for i, j in zip(instances, ids)]

    print("ob", object_ids)
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
        t.stream(data=data, **context).dump(OUTPUT_FOLDER + n_file + ".fsh")


if __name__ == "__main__":
    major_name = DATA_FILE.lower().split("/")[-1].split(".")[0].replace(" ", "_")
    real_output_folder = OUTPUT_FOLDER + major_name + "-ema-automatic/"

    env = create_env(TEMPLATE_FOLDER=TEMPLATE_FOLDER)
    create_from_template(
        env,
        DATA_FILE=DATA_FILE,
        TEMPLATE_FOLDER=TEMPLATE_FOLDER,
        OUTPUT_FOLDER=real_output_folder,
        major_name=major_name,
    )
    quality_checks(
        DATA_FILE=DATA_FILE, OUTPUT_FOLDER=real_output_folder, major_name=major_name
    )
