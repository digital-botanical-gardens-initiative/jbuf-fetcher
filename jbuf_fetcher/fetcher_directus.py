import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

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


# Define the Directus URLs
field_name = "qfield_project"
base_url = "https://emi-collection.unifr.ch/directus"
collection_url = base_url + "/items/Field_Data"
projects_filter = ",".join(project_names)
request_url = (
    collection_url
    + f"?filter[{field_name}][_in]={projects_filter}&&limit=-1&fields=sample_id,sample_name,taxon_name,name_proposition,qfield_project"
)

# Define session
session = requests.Session()

# Extract list from directus
params = {"sort[]": f"-{field_name}"}
response = session.get(request_url, params=params)

if response.status_code == 200:
    # list_directus = response.json()["data"][0][field_name] if response.json()["data"] else "null"
    data_list = response.json().get("data", [])
    # Dictionary for unique sample name
    unique_samples: dict[str, dict[str, str]] = {}

    # Merge taxon_name and sample_name
    filtered_data = []
    for entry in data_list:
        project = entry.get("qfield_project")
        sample_id = entry.get("sample_id")
        sample_name = (entry.get("sample_name") or "").strip()
        taxon_name = (entry.get("taxon_name") or "").strip()
        name_proposition = (entry.get("name_proposition") or "").strip()

        # Replace "aaunknown" (no name on the list)
        if sample_name.lower() == "aaunknown":
            if name_proposition:
                sample_name = name_proposition
            else:
                continue  # ignore the line

        # Merge taxon_name with sample_name
        if not sample_name:
            sample_name = taxon_name

        # If no taxon_name and no sample_name take name_proposition
        if not sample_name:
            sample_name = name_proposition

        # Do not get the line if there is no sample_name
        if sample_name:
            filtered_data.append({"sample_name": sample_name, "sample_id": sample_id, "qfield_project": project})

    # Path file
    data_folder = os.getenv("DATA_PATH", ".")
    os.makedirs(data_folder, exist_ok=True)
    data_file = os.path.join(data_folder, "directus_data.json")

    # Save filtered data
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(filtered_data, f, indent=4)

    print(f"Data have been succesfully saved in {data_file}")

else:
    print(f"error retreiving data: {response.status_code} - {response.text}")
