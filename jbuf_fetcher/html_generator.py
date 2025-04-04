import json
import os
from datetime import datetime
from typing import Any, Callable, cast

from dotenv import load_dotenv
from yattag import Doc

load_dotenv()


# Generate homepage
def generate_homepage() -> None:
    # Get constructors
    doc, tag, text = Doc().tagtext()

    # Make header
    create_html_header(tag, text)

    # Create buttons
    create_html_buttons(tag, text)

    # Add projects
    create_html_projects(tag, text)

    # Write the HTML file
    write_html_file(doc.getvalue())


# Create the HTML header
def create_html_header(tag: Callable[..., Any], text: Callable[[str], None]) -> None:
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


# Create services buttons with icons
def create_html_buttons(tag: Callable[..., Any], text: Callable[[str], None]) -> None:
    # Construct buttons with icons
    buttons = {
        "Directus": {"url": "https://emi-collection.unifr.ch/directus", "icon": "images/directus.png"},
        "NextCloud": {"url": "https://emi-collection.unifr.ch/nextcloud", "icon": "images/nextcloud.png"},
        "QFieldCloud": {"url": "https://emi-collection.unifr.ch/qfieldcloud", "icon": "images/qfieldcloud.png"},
    }

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


# Load json report
def load_json_report() -> dict[str, Any]:
    # Get data folder from .env
    data_folder = os.getenv("DATA_PATH") or ""

    # Construct report path
    json_path = os.path.join(data_folder, "report.json")

    # Try to load json file
    try:
        with open(json_path, encoding="utf-8") as file:
            return cast(dict[str, Any], json.load(file))
    except FileExistsError:
        print(f"Error : the json file '{json_path}' does not exist")
        exit()
    except json.JSONDecodeError:
        print(f"Error : Unable to decode JSON file {json_path} ")
        exit()


# Generate projects
def create_html_projects(tag: Callable[..., Any], text: Callable[[str], None]) -> None:
    # Get report
    report_data = load_json_report()

    # Create containers for projects
    for project_name, project_data in report_data.items():
        # Construct each project
        create_html_project_container(tag, text, project_name, project_data)


# Generate the HTML for each project
def create_html_project_container(
    tag: Callable[..., Any], text: Callable[[str], None], project_name: str, project_data: dict[str, Any]
) -> None:
    # Create a container for each project
    with tag("div", klass="container"):
        # Create header
        create_project_header(tag, text, project_name)

        # Create progressbar
        percentages = project_data.get("percentages", {})
        create_project_progressbar(tag, text, percentages)

        # Create details
        create_project_details(tag, text, project_name, project_data)


def create_project_header(tag: Callable[..., Any], text: Callable[[str], None], project_name: str) -> None:
    # Put title
    with tag("h2"):
        text(f"Collection status for {project_name}")

    # Put update date
    with tag("p", klass="small-text"):
        text(f'(Last update on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")})')


def create_project_progressbar(
    tag: Callable[..., Any], text: Callable[[str], None], percentages: dict[str, float]
) -> None:
    # Get the percentages value
    collected_percent = percentages.get("collected_percent", 0)
    extracted_percent = percentages.get("extracted_percent", 0)
    profiled_percent = percentages.get("profiled_percent", 0)

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


def create_project_details(
    tag: Callable[..., Any], text: Callable[[str], None], project_name: str, project_data: dict[str, Any]
) -> None:
    # Details button
    with tag("button", klass="details-button", onclick=f"toggleDetails({project_name})"):
        text("Details")

    # Details section to be displayed when clicked
    with tag("div", klass="details-container", id=f"details-{project_name}"), tag("h1"):
        text(f"Additional details for project {project_name}:")

        # Not resolved data list
        with tag("h1"):
            text(f"Not resolved Data for {project_name}")

        # Get the unresolved list
        not_resolved_directus = project_data.get("not_resolved_directus", [])
        not_resolved_botavista = project_data.get("not_resolved_botavista", [])

        # List not_resolved_directus
        if not_resolved_directus:
            with tag("h4"):
                text("Not Resolved Directus:")
            with tag("ul"):
                for item in not_resolved_directus:
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


def write_html_file(content: str) -> None:
    # Get html folder from .env
    html_folder = os.getenv("HTML_PATH") or ""

    # Create html path
    html_file = os.path.join(html_folder, "home_page.html")

    # Create file
    with open(html_file, "w") as file:
        file.write(content)

    print("Responsive HTML file generated successfully!")


# Generate the homepage
generate_homepage()
