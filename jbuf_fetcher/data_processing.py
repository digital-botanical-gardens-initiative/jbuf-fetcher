import json
import os
from typing import Any

import pandas as pd
from dotenv import load_dotenv

from jbuf_fetcher import utils

load_dotenv()

# Get the data lists
data_folder = os.getenv("DATA_PATH") or ""
file_path_directus = os.path.join(data_folder, "resolved_data_directus.json")
file_path_botavista = os.path.join(data_folder, "resolved_data_botavista.json")

# Get the project mappings
garden_name = utils.get_garden_names()
botavista_code = utils.get_botavista_codes()
qfield_code = utils.get_qfield_codes()


# Function to load JSON data into a DataFrame
def load_json_as_df(file_path: str) -> pd.DataFrame:
    # Check if the file exists
    if os.path.exists(file_path):
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)
        return pd.DataFrame(data)
    else:
        print(f"Error : the file {file_path} does not exist")
        exit()


# Function to create the report
def create_report(df_botavista: pd.DataFrame, df_directus: pd.DataFrame) -> None:
    # Get merged data
    merged_df = create_merged_df(df_botavista, df_directus)

    # Create array to store the global report
    report = {}

    # Get projects list
    projects = utils.get_qfield_codes()

    # Create the global report
    for project in projects:  # Loop through each project
        # Get project data
        project_df = merged_df[merged_df["qfield_project"] == project]

        # Get project report
        project_report = get_project_report(project_df, project)

        # Append project report to the global report
        report[project] = project_report

    # Generate json report
    write_json_report(report)


# Preparing df
def create_merged_df(df_botavista: pd.DataFrame, df_directus: pd.DataFrame) -> pd.DataFrame:
    # Optionnel : répertoire de sortie
    data_path = os.getenv("DATA_PATH") or ""
    debug_dir = os.path.join(data_path, "debug")
    os.makedirs(debug_dir, exist_ok=True)

    # Drop unnecessary columns
    df_botavista = df_botavista.drop(["submitted_name", "resolution_confidence"], axis=1)
    df_directus = df_directus.drop(["species", "submitted_name", "resolution_confidence"], axis=1)

    # Ensure unique species per project (one entry per species per project)
    df_botavista = df_botavista.drop_duplicates(subset=["resolved_species", "qfield_project"])
    df_directus = df_directus.drop_duplicates(subset=["resolved_species", "qfield_project"])

    # Perform the merge
    merged_df = pd.merge(
        df_botavista, df_directus, on=["resolved_species", "qfield_project"], how="outer", indicator="indicator"
    )

    return merged_df


# Count the matched and unmatched species
def get_project_report(merged_df: pd.DataFrame, project: str) -> dict[str, Any]:
    # Column indicator
    column = "indicator"

    # Get counts of each category
    counts = merged_df[column].value_counts()

    # Separate df following wanted categories and drop unnecessary columns
    matched_df = merged_df[merged_df[column] == "both"]
    directus_only_df = merged_df[merged_df[column] == "right_only"].drop(
        ["qfield_project", "indicator", "locations", "species"], axis=1
    )
    botavista_only_df = merged_df[merged_df[column] == "left_only"].drop(
        ["qfield_project", "sample_id", "extracted", "profiled", "indicator"], axis=1
    )

    # Assign values
    total_available = int(counts.get("both", 0) + counts.get("left_only", 0))
    total_collected = int(counts.get("both", 0))
    total_extracted = matched_df["extracted"].sum()
    total_profiled = matched_df["profiled"].sum()
    botavista_only = int(counts.get("left_only", 0))
    directus_only = int(counts.get("right_only", 0))
    directus_only_json = directus_only_df.to_dict(orient="records")
    botavista_only_json = botavista_only_df.to_dict(orient="records")

    # Get percentages
    percentages = (
        {
            "collected_percent": total_collected / total_available * 100,
            "extracted_percent": total_extracted / total_available * 100,
            "profiled_percent": total_profiled / total_available * 100,
        }
        if total_available > 0
        else {
            "collected_percent": 0,
            "extracted_percent": 0,
            "profiled_percent": 0,
        }
    )

    # Get unresolved data
    not_resolved_directus, not_resolved_botavista = get_unresolved_data(project)

    # Format data
    data_json = {
        "total_available": total_available,
        "total_collected": total_collected,
        "total_extracted": total_extracted,
        "total_profiled": total_profiled,
        "percentages": percentages,
        "to_collect": botavista_only,
        "to_collect_json": botavista_only_json,
        "no_more_in_garden": directus_only,
        "no_more_in_garden_json": directus_only_json,
        "not_resolved_botavista": not_resolved_botavista,
        "not_resolved_directus": not_resolved_directus,
    }

    # Add project as key
    final_json = data_json

    return final_json


# Get de unresolved json
def get_unresolved_data(project: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    # Construct files paths
    file_path_directus_not_resolved = os.path.join(data_folder, "not_resolved_data_directus.json")
    file_path_botavista_not_resolved = os.path.join(data_folder, "not_resolved_data_botavista.json")

    # Load jsons
    with open(file_path_directus_not_resolved, encoding="utf-8") as f:
        data_directus_unresolved = json.load(f)

    with open(file_path_botavista_not_resolved, encoding="utf-8") as f:
        data_botavista_unresolved = json.load(f)

    # Filter data by project
    filtered_directus = [item for item in data_directus_unresolved if item.get("qfield_project") == project]
    filtered_botavista = [item for item in data_botavista_unresolved if item.get("qfield_project") == project]

    return filtered_directus, filtered_botavista


# Write json report
def write_json_report(report: dict[Any, dict[str, Any]]) -> None:
    # Json path
    json_path = os.path.join(data_folder, "report.json")

    # Wirte json
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

    print(f"✅ JSON generate successfully : {json_path}")


# Load data
df_botavista = load_json_as_df(file_path_botavista)
df_directus = load_json_as_df(file_path_directus)

# Create the report
create_report(df_botavista, df_directus)
