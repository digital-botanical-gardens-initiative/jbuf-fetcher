import json
import os
from datetime import datetime
from typing import Any, cast

from dotenv import load_dotenv
from yattag import Doc

load_dotenv()

# Get the folder from .env
data_folder = os.getenv("DATA_PATH") or ""
html_folder = os.getenv("HTML_PATH") or ""


# Get projects
project = os.getenv("PROJECT", "").split(",")


# Function to load the report json
def load_report_json() -> dict[str, Any]:
    json_path = os.path.join(data_folder, "report.json")
    try:
        with open(json_path, encoding="utf-8") as file:
            return cast(dict[str, Any], json.load(file))
    except FileExistsError:
        print(f"Error : the json file '{json_path}' does not exist")
        return {}
    except json.JSONDecodeError:
        print(f"Error : Unable to decode JSON file {json_path} ")
        return {}


report_data = load_report_json()


# Style
# Path to css file
css_path = os.path.relpath("styles.css")

if not os.path.exists(css_path):
    print("ERROR : the file does not exist at this location")
else:
    print(" The file is present at this location")


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

    # Create containers for projects
    # for project in report_data:
    for project_name, project_data in report_data.items():
        # Get the percentages value
        percentages = project_data.get("percentages", {})
        collected_percent = percentages.get("collected_percent", 0)
        extracted_percent = percentages.get("extracted_percent", 0)
        profiled_percent = percentages.get("profiled_percent", 0)

        # Create a container for each project
        with tag("div", klass="container"):
            with tag("h2"):
                text(f"Collection status for {project_name}")

            #     # Update date
            with tag("p", klass="small-text"):
                text(f'(Last update on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")})')

            # Create progressbar
            with tag("div", klass="progress-container"):
                with tag("div", klass="progress-bar collected", style=f"width: {collected_percent}%"):
                    pass
                with tag("div", klass="progress-bar extracted", style=f"width: {extracted_percent}%"):
                    pass
                with tag("div", klass="progress-bar profiled", style=f"width: {profiled_percent}%"):
                    pass

            # Add a legend
            with tag("div", klass="legend"):
                with tag("div", klass="legend-item"):
                    with tag("span", klass="legend-circle", style="background-color: #00e600;"):
                        pass
                    with tag("span", klass="legend-text"):
                        text(f"Profiled ({profiled_percent:.1f}%)")

                with tag("div", klass="legend-item"):
                    with tag("span", klass="legend-circle", style="background-color: #ffee00;"):
                        pass
                    with tag("span", klass="legend-text"):
                        text(f"Extracted ({extracted_percent:.1f}%)")

                with tag("div", klass="legend-item"):
                    with tag("span", klass="legend-circle", style="background-color: #ff9900;"):
                        pass
                    with tag("span", klass="legend-text"):
                        text(f"Collected ({collected_percent:.1f}%)")

            # Details button
            with tag("button", klass="details-button", onclick=f"toggleDetails({project})"):
                text("Details")

            # # Get specific information for each project
            # df = load_json_as_dataframe()
            # project_data = get_project_details(i, df)

            # Details section to be displayed when clicked
            with tag("div", klass="details-container", id=f"details-{project}"), tag("h1"):
                text(f"Additional details for project {project}:")

                # Not resolved data list
                with tag("h1"):
                    text(f"Not resolved Data for {project_name}")

                # Get the unresolved list
                not_resolved_directus = report_data[project_name].get("not_resolved_directus", [])
                not_resolved_botavista = report_data[project_name].get("not_resolved_botavista", [])

                # List not_resolved_directus
                if not_resolved_directus:
                    with tag("h4"):
                        text("Not Resolved Directus:")
                    with tag("ul"):
                        for item in not_resolved_directus:
                            print(item)
                            with tag("li"):
                                text(str(item))

                # List not_resolved_botavista
                if not_resolved_botavista:
                    with tag("h4"):
                        text("Not Resolved Botavista:")
                    with tag("ul"):
                        for item in not_resolved_botavista:
                            with tag("li"):
                                text(str(item))

            #         # list
            #         if not project_data.empty:
            #             with tag("ul"):
            #                 for _, row in project_data.iterrows():
            #                     with tag("li"):
            #                         with tag("strong"):
            #                             text(f"Sample Name: {row['species']}")
            #                         with tag("ul"):
            #                             for key, value in row.items():
            #                                 if key != "species":
            #                                     with tag("li"):
            #                                         text(f"{key}: {value}")

            #         else:
            #             with tag("p"):
            #                 text("No suplementary data for this project.")

    return doc.getvalue()


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
