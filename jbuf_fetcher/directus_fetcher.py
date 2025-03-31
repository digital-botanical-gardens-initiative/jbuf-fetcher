import json
import os
import re

import requests
from dotenv import load_dotenv

load_dotenv()

# Define session
session = requests.Session()

# Directus url
base_url = "https://emi-collection.unifr.ch/directus"

project_dict_str = os.getenv("PROJECT")

if not project_dict_str:
    print("Error : variable PROJECT not specified in .env")
    exit()

try:
    # Convert JSON to python dictionary
    project_dict = json.loads(project_dict_str)
except json.JSONDecodeError:
    print("Error: PROJECT variable in .env is not a valid JSON")
    exit()

# Extract only the key (project name)
project_names = list(project_dict.keys())

# Check if there are some projects
if not project_names:
    print("No project found in .env")
    exit()


def get_data() -> None:
    # Make directus request
    field_name = "qfield_project"
    collection_url = base_url + "/items/Field_Data"
    projects_filter = ",".join(project_names)
    request_url = (
        collection_url
        + f"?filter[{field_name}][_in]={projects_filter}&&limit=-1&fields=sample_id,sample_name,taxon_name,name_proposition,qfield_project"
    )

    # Extract list from directus
    params = {"sort[]": f"-{field_name}"}
    response = session.get(request_url, params=params)

    if response.status_code == 200:
        data_list = response.json().get("data", [])
        parse_data(data_list)

    else:
        print(f"error retreiving data: {response.status_code} - {response.text}")
        exit()


def parse_data(data_list: dict) -> None:
    # Merge taxon_name and sample_name
    filtered_data = []
    # sample_id correct pattern
    pattern = r"^[A-Za-z]{3,}_[0-9]{6}$"

    for entry in data_list:
        project = entry.get("qfield_project")
        sample_id = entry.get("sample_id").replace(" ", "")
        sample_name = (entry.get("sample_name") or "").strip()
        taxon_name = (entry.get("taxon_name") or "").strip()
        name_proposition = (entry.get("name_proposition") or "").strip()

        # If sample_id doesn't match pattern, ignore sample
        if not re.match(pattern, sample_id):
            continue

        # Check if sample is extracted and/or profiled
        extracted, profiled = is_treated(sample_id)

        # Merge taxon_name with sample_name
        if not sample_name:
            sample_name = taxon_name

        # If no taxon_name and no sample_name take name_proposition
        if not sample_name:
            sample_name = name_proposition

        # Do not get the line if there is no sample_name
        if sample_name:
            filtered_data.append({
                "species": sample_name,
                "sample_id": sample_id,
                "qfield_project": project,
                "extracted": extracted,
                "profiled": profiled,
            })

    # Path file
    data_folder = os.getenv("DATA_PATH", ".")
    os.makedirs(data_folder, exist_ok=True)
    data_file = os.path.join(data_folder, "directus_data.json")

    # Save filtered data
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(filtered_data, f, indent=4)

    print(f"Data have been succesfully saved in {data_file}")


def is_treated(sample_id: str) -> tuple[bool, bool]:
    container_id = get_container_id(sample_id)
    if container_id == 0:
        return False, False

    # Check if the sample is extracted
    extracted = get_child_container_id(container_id, "Extraction_Data", "sample_container")
    if extracted == 0:
        return False, False

    # Check if the sample is aliquoted
    aliquoted = get_child_container_id(extracted, "Aliquoting_Data", "sample_container")
    if aliquoted == 0:
        return True, False

    # Check if the sample is profiled
    profiled = get_child_container_id(aliquoted, "MS_Data", "id")
    return True, profiled != 0


def get_child_container_id(container_id: int, collection: str, field_of_interest: str) -> int:
    # Make directus request
    field_name = "parent_sample_container"
    collection_url = base_url + "/items/" + collection
    request_url = collection_url + f"?filter[{field_name}][_eq]={container_id}&&limit=1&fields={field_of_interest}"

    # Extract list from directus
    response = session.get(request_url)

    if response.status_code == 200:
        if response.json()["data"] == []:
            return 0
        else:
            child_container_id = int(response.json()["data"][0][field_of_interest])
            return child_container_id
    else:
        print(f"Error: status: {response.status_code} - message: {response.text}")
        exit()


def get_container_id(sample_id: str) -> int:
    # Make directus request
    field_name = "container_id"
    collection_url = base_url + "/items/Containers"
    request_url = collection_url + f"?filter[{field_name}][_eq]={sample_id}&&limit=1&fields=id"

    # Extract list from directus
    response = session.get(request_url)

    if response.status_code == 200:
        if response.json()["data"] != []:
            container_id = int(response.json()["data"][0]["id"])
            return container_id
        else:
            return 0

    else:
        print(f"Error: status: {response.status_code} - message: {response.text}")
        exit()


get_data()
