import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

# Define the Directus URLs
field_name = "qfield_project"
base_url = "https://emi-collection.unifr.ch/directus"
project = "jbuf"
collection_url = base_url + "/items/Field_Data"
request_url = collection_url + f"?filter[{field_name}][_eq]={project}&&limit=-1"

# Define session
session = requests.Session()

# Extract list from directus
params = {"sort[]": f"-{field_name}"}
response = session.get(request_url, params=params)

if response.status_code == 200:
    # list_directus = response.json()["data"][0][field_name] if response.json()["data"] else "null"
    data_list = response.json().get("data", [])
    # print(list_directus)

    # Merge taxon_name and sample_name
    filtered_data = [{"sample_name": entry.get("sample_name") or entry.get("taxon_name", "")} for entry in data_list]

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
