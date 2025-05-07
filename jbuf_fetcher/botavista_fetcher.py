import io
import json
import os
import zipfile
from io import BytesIO, StringIO

import pandas as pd
import requests
from dotenv import load_dotenv

from jbuf_fetcher import utils

load_dotenv()


# Extract botavista names
botavista_codes = utils.get_botavista_codes()

# Define session
session = requests.Session()

# Creat json array
json_file = []

# Loop over projects
for code in botavista_codes:
    # Construct url
    url = f"https://botavista.com/csv/{code.upper()}"
    response = session.get(url)
    print(f"Téléchargement de: https://botavista.com/csv/{code.upper()}")

    if response.status_code == 200:
        try:
            with zipfile.ZipFile(BytesIO(response.content)) as z:
                print(f"{code}: Contenu du ZIP: {z.namelist()}")
                csv_filename = z.namelist()[0]
                # Unzip the ZIP file in memory
                with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                    csv_filename = z.namelist()[0]
                    with z.open(csv_filename) as f:
                        content = f.read().decode("utf-8", errors="ignore")

                        if content.strip().startswith("<!DOCTYPE html>") or "Error" in content:
                            print(f"{code} returned an error page instead of CSV.")
                            continue

                        csv_io = StringIO(content)
                        df = pd.read_csv(csv_io, sep=";", encoding="utf-8", engine="python", on_bad_lines="skip")

                        if df.empty:
                            print(f"{code} returned an empty CSV file and is ignored.")
                            continue

                        colname = "acquisitionName"
                        if colname not in df.columns:
                            print(f"{code} does not contain the column {colname}.")
                            continue

                        # Aadapt this part to the CSV structure
                        grouped = df.groupby(colname)

                        for species, group in grouped:
                            locations = group["place"].dropna().unique().tolist()
                            element = {
                                "species": species,
                                "qfield_project": utils.get_qfield_code_from_botavista_code(code),
                                "locations": locations,
                            }
                            json_file.append(element)
            print(f"{code} correctly fetched")
        except Exception as e:
            print(f"{code} ignoré (erreur: {e})")
            continue
    else:
        print(f"{code} ignored (status code: {response.status_code})")
        continue
# Save the JSON file
data_path = str(os.getenv("DATA_PATH"))
file_path = os.path.join(data_path, "botavista_data.json")

with open(file_path, "w") as f:
    json.dump(json_file, f, indent=4)
