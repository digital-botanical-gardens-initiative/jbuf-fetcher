import json
import os
from typing import cast

import requests
from dotenv import load_dotenv

load_dotenv()

# project_dict_str = os.getenv("PROJECT")

# if not project_dict_str:
#     print("Error : variable PROJECT not specified in .env")
#     exit()

# try:
#     # Convert JSON to python dictionary
#     project_dict = json.loads(project_dict_str)
# except json.JSONDecodeError:
#     print("Error: PROJECT variable in .env is not a valid JSON")
#     exit()

# # Extract botavista names
# botavista_codes = list(project_dict.values())

# # Check if there are some projects
# if not botavista_codes:
#     print("No project found in .env")
#     exit()


# Load project mappings from project_mappings.json
def load_project_mappings() -> dict[str, dict[str, str]]:
    # Path to the JSON file
    data_path = os.getenv("DATA_PATH", "")
    mappings_file = os.path.join(data_path, "project_mappings.json")

    # Check if the file exists
    if not os.path.exists(mappings_file):
        print(f"Error: The mappings file '{mappings_file}' does not exist.")
        exit()

    # Load the JSON file
    try:
        with open(mappings_file, encoding="utf-8") as file:
            # Load the entire JSON structure
            data = json.load(file)
            # Ensure the data is a dictionary with the expected structure
            return cast(dict[str, dict[str, str]], data)
    except FileNotFoundError:
        print(f"Error: The mappings file '{mappings_file}' does not exist.")
        exit()
    except json.JSONDecodeError:
        print(f"Error: Unable to decode JSON file '{mappings_file}'.")
        exit()


# Load the project dictionary
project_dict = load_project_mappings()

# Extract botavista names
botavista_codes = {key: value["botavista_code"] for key, value in project_dict.items()}

# Check if there are some projects
if not botavista_codes:
    print("No project found in project_mappings.json")
    exit()


# Define session
session = requests.Session()

# Creat json array
json_file = []

# Loop over projects
for _project_name, code in botavista_codes.items():
    # Construct url
    url = f"https://botavista.com/api/cultivated/search/{code}?query=s"
    response = session.get(url)
    if response.status_code == 200:
        if len(response.json()["data"]["aggregations"]["codeBcgi"]) == 1:
            retrieved_code = response.json()["data"]["aggregations"]["codeBcgi"][0]["key"]
            if code.upper() == retrieved_code.upper():
                data = response.json()["data"]["results"]
                for species in range(len(data)):
                    sci_name = data[species]["name"]
                    species_list = data[species]["list"]
                    locations = []
                    for specimen in range(len(species_list)):
                        location = species_list[specimen]["place"]
                        locations.append(location)
                    element = {
                        "species": sci_name,
                        "qfield_project": next(
                            (k for k, v in project_dict.items() if v["botavista_code"] == code), None
                        ),
                        "locations": locations,
                    }
                    json_file.append(element)

                print(f"{code} correctly fetched")

            else:
                print(f"{code} doesn't match {retrieved_code}")
        else:
            print(f"{code} seems to be absent from botavista")
    else:
        print(f"Error accessing data for {code}")

data_path = str(os.getenv("DATA_PATH"))
file_path = os.path.join(data_path, "botavista_data.json")

# Write back to the file
with open(file_path, "w") as f:
    json.dump(json_file, f, indent=4)
