import json
import os

import requests

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
    list_directus = response.json()["data"][0][field_name] if response.json()["data"] else "null"
    # print(list_directus)

    data_folder = "../data"
    data_file = os.path.join(data_folder, "directus_data.json")
    print(data_file)

    list_directus = response.json().get("data", [])

    # Sauve data
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(list_directus, f, indent=4)

    print(f"Data have been succesfully saved in {data_file}")

else:
    print(f"error retreiving data: {response.status_code} - {response.text}")
