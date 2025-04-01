import json
import os

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Get the data lists
data_folder = os.getenv("DATA_PATH") or ""
file_path_directus = os.path.join(data_folder, "resolved_data_directus.json")
file_path_botavista = os.path.join(data_folder, "resolved_data_botavista.json")

# Get projects
projects = json.loads(str(os.getenv("PROJECT")))


def load_json_as_df(file_path: str) -> pd.DataFrame:
    if os.path.exists(file_path):
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)
        print(f"{file_path} successfully charged")
        return pd.DataFrame(data)
    else:
        print(f"Error : the file {file_path} does not exist")
        exit()


def create_report() -> None:
    # Load data
    df_botavista = load_json_as_df(file_path_botavista)
    df_directus = load_json_as_df(file_path_directus)

    # Drop unnecessary columns
    df_botavista = df_botavista.drop(["species", "submitted_name", "resolution_confidence"], axis=1)
    df_directus = df_directus.drop(["species", "submitted_name", "resolution_confidence"], axis=1)

    # Ensure unique species per project (one entry per species per project)
    df_botavista = df_botavista.drop_duplicates(subset=["resolved_species", "qfield_project"])
    df_directus = df_directus.drop_duplicates(subset=["resolved_species", "qfield_project"])

    merged_df = pd.merge(
        df_botavista, df_directus, on=["resolved_species", "qfield_project"], how="outer", indicator="indicator"
    )
    print(merged_df[merged_df["indicator"] == "both"])


create_report()
