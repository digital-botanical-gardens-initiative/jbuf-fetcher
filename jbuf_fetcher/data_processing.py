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


# Preparing df
def create_merged_df() -> tuple[pd.DataFrame, pd.DataFrame]:
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
    # print(merged_df[merged_df["indicator"] == "right_only"])
    return merged_df, df_botavista


# Count the matched and unmatched species
def count_indicator(merged_df: pd.DataFrame, column: str = "indicator") -> dict[str, int]:
    counts = merged_df[column].value_counts()

    matched_df = merged_df[merged_df[column] == "both"]
    matched_extracted = matched_df["extracted"].sum()
    matched_profiled = matched_df["profiled"].sum()

    return {
        "matched": int(counts.get("both", 0)),
        "botavista_only": int(counts.get("left_only", 0)),
        "directus_only": int(counts.get("right_only", 0)),
        "matched_extracted": matched_extracted,
        "matched_profiled": matched_profiled,
    }


# Get the % for the progress bar
def calculate_percentages(df_botavista: pd.DataFrame, report: dict[str, int]) -> dict[str, int]:
    total = len(df_botavista)

    if total == 0:  # avoid dividing by 0
        return {
            "matched_percent": 0,
            "matched_extracted_percent": 0,
            "matched_profiled_percent": 0,
        }

    return {
        "matched_percent": int(round((report["matched"] / total) * 100)),
        "matched_extracted_percent": int(round((report["matched_extracted"] / total) * 100)),
        "matched_profiled_percent": int(round((report["matched_profiled"] / total) * 100)),
    }


# Global function
def create_report() -> dict[str, dict[str, int]]:
    merged_df, df_botavista = create_merged_df()
    report_per_project = {}
    unique_project = merged_df["qfield_project"].unique()

    for project in unique_project:
        project_df = merged_df[merged_df["qfield_project"] == project]
        project_percentages = df_botavista[df_botavista["qfield_project"] == project]

        report = count_indicator(project_df)
        percentages = calculate_percentages(project_percentages, report)
        report.update(percentages)

        report_per_project[str(project)] = report

    return report_per_project


final_report = create_report()
print(final_report)
