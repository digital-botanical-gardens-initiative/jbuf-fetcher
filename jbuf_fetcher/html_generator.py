import json
import os
from datetime import datetime
from typing import Any

import pandas as pd
from dotenv import load_dotenv
from yattag import Doc

load_dotenv()

data_folder = os.getenv("DATA_PATH") or ""
html_folder = os.getenv("HTML_PATH") or ""


# Not resolved data
# Get json for not resolved data
def load_json_as_dataframe() -> pd.DataFrame:
    json_file_path = os.path.join(data_folder, "not_resolved_data.json")
    if not os.path.isfile(json_file_path):
        print(f"Error : {json_file_path} is not a valid file.")
        return pd.DataFrame()
    with open(json_file_path, encoding="utf-8") as file:
        data = json.load(file)
    return pd.DataFrame(data)


# Filters the DataFrame to retrieve only entries corresponding to the project
def get_project_details(project_name: str, df: pd.DataFrame) -> pd.DataFrame:
    if not df.empty and "qfield_project" in df.columns:
        return df[df["qfield_project"] == project_name]
    return pd.DataFrame()


# Test json for plants and sectors
CSV_FILE = "species_list.csv"
JSON_FILE = os.path.join(data_folder, "filtered_sector_data.json")

try:
    df = pd.read_csv(CSV_FILE, usecols=["idTaxon", "secteur"])
except ValueError:
    print("Columns do not exist")

df = df.head(30)
sector_plant_list = df.to_dict(orient="records")

os.makedirs(data_folder, exist_ok=True)

# Convert in Json
with open(JSON_FILE, "w", encoding="utf-8") as json_file:
    json.dump(sector_plant_list, json_file, ensure_ascii=False, indent=4)

if not os.path.exists(JSON_FILE):
    print(f"The file {JSON_FILE} does not exist in {data_folder}.")
if os.path.getsize(JSON_FILE) == 0:
    print(f"The file is empty : {JSON_FILE}")

with open(JSON_FILE, encoding="utf-8") as json_file, open(JSON_FILE, encoding="utf-8") as json_file:
    data_sector = json.load(json_file)


print(f"Le fichier JSON a été créé et sauvegardé sous : {JSON_FILE}")

# Organise by sectors
secteurs_dict: dict[str, list[Any]] = {}
for record in data_sector:
    secteur = record.get("secteur")
    if secteur:
        if secteur not in secteurs_dict:
            secteurs_dict[secteur] = []
        secteurs_dict[secteur].append(record)

# Style
# Path to css file
css_path = os.path.relpath("styles.css")

if not os.path.exists(css_path):
    print("❌ ERREUR : Le fichier CSS n'existe pas à cet emplacement !")
else:
    print("✅ Le fichier CSS est bien présent.")


# Generate homepage
def generate_homepage(buttons: dict, data_path: str) -> str:
    doc, tag, text = Doc().tagtext()

    with tag("html"), tag("head"):
        with tag("title"):
            text("Home")
        with (
            tag("meta", name="viewport", content="width=device-width, initial-scale=1.0"),
            tag(
                "link",
                rel="stylesheet",
                href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",
            ),
            # Lien vers le fichier CSS externe
            tag("link", rel="stylesheet", href="styles.css"),
        ):
            pass

    # # Viewport for responsiveness
    # with (
    #     tag("meta", name="viewport", content="width=device-width, initial-scale=1.0"),
    #     tag(
    #         "link",
    #         rel="stylesheet",
    #         href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",
    #     ),
    #     tag("style"),
    # ):

    #     text("""
    #         /* Global Reset */
    #         * { margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, sans-serif; text-align: center; }

    #         /* Centered container */
    #         .container { width: 100%; margin: 20px auto; padding: 20px; border-radius: 40px; background: #d7dfd3; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); }

    #         /* Button Container */
    #         .button-container {
    #             display: flex;
    #             justify-content: space-between;
    #             gap: 2%;
    #             margin-top: 20px;
    #             flex-wrap: nowrap;
    #         }
    #         .button {
    #             flex: 1;
    #             padding: 10px 0;
    #             font-size: 3vw;
    #             background-color: #5c7444;
    #             color: white;
    #             border: 40px;
    #             border-radius: 40px;
    #             cursor: pointer;
    #             text-decoration: none;
    #             display: flex;
    #             flex-direction: column;
    #             align-items: center;
    #             justify-content: center;
    #             transition: background-color 0.3s;
    #         }
    #         .button:hover { background: #94a58c; }

    #         /* Icon Styling */
    #         .button img, .button i {
    #             width: 5vw;
    #             height: 5vw;
    #         }

    #         .list {
    #             border: 1px solid #ddd;
    #             padding: 20px;
    #             border-radius: 5px;
    #             background: #f9f9f9;
    #             text-align: left;
    #         }

    #         /* Responsive Design */
    #         @media (max-width: 1000px) {
    #             .button { width: 100%; justify-content: center; }
    #         }

    #         .progress-container {
    #             width: 100%;
    #             height: 30px;
    #             background-color: #fff;  /* white background */
    #             border-radius: 20px;
    #             position: relative;
    #             box-sizing: border-box;
    #             margin-bottom: 10px; /* Espacement entre les projets */
    #         }

    #         .progress-bar {
    #             height: 100%;
    #             border-radius: 20px;
    #             position: absolute;
    #             top: 0;
    #         }

    #         /* Specific color for each status*/
    #         .collected {
    #             background-color: #ff9900;
    #             height: 30px;
    #         }

    #         .extracted {
    #             background-color: #ffee00;
    #             height: 25px;
    #         }

    #         .profiled {
    #             background-color: #00e600;
    #             height: 20px;
    #         }

    #         .small-text {
    #             font-size: 15px;
    #             color: #888;
    #             margin-bottom: 15px;
    #         }

    #         .legend {
    #             display: flex;
    #             justify-content: space-around;
    #             margin-top: 10px;
    #         }

    #         .legend-item {
    #             display: flex;
    #             align-items: center;
    #         }

    #         .legend-circle {
    #             width: 12px;
    #             height: 12px;
    #             border-radius: 50%;
    #             margin-right: 5px;
    #         }

    #         .legend-text {
    #             font-size: 14px;
    #         }

    #         .details-container {
    #             font-size: 14px;
    #             display: none;
    #             margin-top: 10px;
    #             padding: 10px;
    #             background-color: #f9f9f9;
    #             border-radius: 8px;
    #             box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    #             text-align: left;
    #             line-height: 1.7;

    #         }

    #          /* title details */
    #         .details-container h2 {
    #             font-size: 30px;
    #             font-weight: bold;
    #             margin-bottom: 15px;
    #         }
    #         .details-container h3 {
    #             font-size: 20px;
    #             font-weight: bold;
    #             margin-bottom: 15px;
    #         }

    #         .details-container ul {
    #             font-size: 15px;
    #             font-weight: bold;
    #             margin-bottom: 15px;
    #         }

    #         .details-container.open {
    #             display: block;
    #             height: auto;
    #             transition: all 0.3s ease-in-out;
    #         }

    #         .details-button {
    #             padding: 10px;
    #             background-color: #5c7444;
    #             color: white;
    #             border: none;
    #             border-radius: 40px;
    #             cursor: pointer;
    #             font-size: 14px;
    #             margin-top: 10px;
    #         }

    #         .details-button:hover {
    #             background-color: #94a58c;
    #         }

    #         .details-container .sample-name {
    #             font-weight: bold; /* Met en gras le contenu */
    #         }
    #         """)
    # Add JavaScript to manage display
    with tag("script"):
        doc.asis("""
             function toggleDetails(idx) {
                 var detailsContainer = document.getElementById('details-' + idx);
                 detailsContainer.classList.toggle('open');
             }
         """)
    # Button container
    with tag("body"), tag("div", klass="container"):
        with tag("h1"):
            text("Services")

        with tag("div", klass="button-container"):
            for button_name, attributes in buttons.items():
                with tag("a", klass="button", href=attributes["url"]):
                    with tag("img", src=attributes["icon"]):
                        pass
                    text(button_name)

    # Get collection data
    # resolved_data = os.path.join(data_path, "resolved_data.json")
    # not_resolved_data = os.path.join(data_path, "not_resolved_data.json")

    # Get projects
    projects = json.loads(str(os.getenv("PROJECT")))

    # Create containers for projects
    for idx, i in enumerate(projects):
        with tag("body"), tag("div", klass="container"), tag("h1"):
            text(f"Collection status {i.upper()}")
            with tag("p", klass="small-text"):
                text(f'(Last update on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")})')

            # Progress bar
            collected = collected_values[idx]
            extracted = extracted_values[idx]
            profiled = profiled_values[idx]

            with tag("div", klass="progress-container"):
                with tag("div", klass="progress-bar collected", style=f"width: {collected}%"):
                    pass
                with tag("div", klass="progress-bar extracted", style=f"width: {extracted}%"):
                    pass
                with tag("div", klass="progress-bar profiled", style=f"width: {profiled}%"):
                    pass

            # Legend
            with tag("div", klass="legend"):
                with tag("div", klass="legend-item"):
                    with tag("span", klass="legend-circle", style="background-color: #00e600;"):
                        pass
                    with tag("span", klass="legend-text"):
                        text(f"Profiled ({profiled}%)")

                with tag("div", klass="legend-item"):
                    with tag("span", klass="legend-circle", style="background-color: #ffee00;"):
                        pass
                    with tag("span", klass="legend-text"):
                        text(f"Extracted ({extracted}%)")

                with tag("div", klass="legend-item"):
                    with tag("span", klass="legend-circle", style="background-color: #ff9900;"):
                        pass
                    with tag("span", klass="legend-text"):
                        text(f"Collected ({collected}%)")
            # Details button
            with tag("button", klass="details-button", onclick=f"toggleDetails({idx})"):
                text("Details")

            # Get specific information for each project
            df = load_json_as_dataframe()
            project_data = get_project_details(i, df)

            # Details section to be displayed when clicked
            with tag("div", klass="details-container", id=f"details-{idx}"):
                with tag("h2"):
                    text(f"Additional details for project {i}:")

                # Test plant by sectors with json
                with tag("h2"):
                    text("Plants to collect by sector")

                for sector, plants in secteurs_dict.items():
                    with tag("h3"):
                        text(f"Plants to collect in {sector}")

                    with tag("ul"):
                        for plant in plants:
                            with tag("li"):
                                text(plant["idTaxon"])

                # Not resolved data list
                with tag("h2"):
                    text("Not resolved Data")
                    if not project_data.empty:
                        with tag("ul"):
                            for _, row in project_data.iterrows():
                                with tag("li"):
                                    text(
                                        f"{row.to_json(indent=2)}"
                                    )  # Afficher chaque ligne du DataFrame sous forme JSON
                    else:
                        with tag("p"):
                            text("No suplementary data for this project.")

    return doc.getvalue()


# Variable progress bar
progress_values = [50, 30]
collected_values = [60, 30]
extracted_values = [40, 15]
profiled_values = [15, 5]


# Generate buttons with icons
buttons = {
    "Directus": {"url": "https://emi-collection.unifr.ch/directus", "icon": "images/directus.png"},
    "NextCloud": {"url": "https://emi-collection.unifr.ch/nextcloud", "icon": "images/nextcloud.png"},
    "QFieldCloud": {"url": "https://emi-collection.unifr.ch/qfieldcloud", "icon": "images/qfieldcloud.png"},
}

# Check that data folder exists
if not data_folder:
    print("Error : no DATA_PATH")
    exit(1)

# Create html path
html_file = os.path.join(html_folder, "home_page.html")

# Generate HTML and save to file
html_content = generate_homepage(buttons, html_folder)
with open(html_file, "w") as file:
    file.write(html_content)

print("Responsive HTML file generated successfully!")
