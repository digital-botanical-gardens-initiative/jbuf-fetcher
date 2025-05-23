import json
import os
from datetime import datetime
from typing import Any, Callable, cast

from dotenv import load_dotenv
from yattag import Doc, SimpleDoc

from jbuf_fetcher import utils

doc, tag, text = Doc().tagtext()


load_dotenv()


# Generate homepage
def generate_homepage() -> None:
    # Get constructors
    doc, tag, text = Doc().tagtext()

    # Make header
    create_html_header(doc, tag, text)

    # Create buttons
    create_html_buttons(tag, text)

    # Add projects
    create_html_projects(tag, text)

    # Allow expand/collapse behaviour
    create_html_script(tag)

    # Write the HTML file
    write_html_file(doc.getvalue())


# Create the HTML header
def create_html_header(doc: SimpleDoc, tag: Callable[..., Any], text: Callable[[str], None]) -> None:
    with tag("html"), tag("head"):
        doc.stag("meta", charset="UTF-8")
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


def create_html_script(tag: Callable[..., Any]) -> None:
    with tag("script", src="scripts.js"):
        pass


# Create services buttons with icons
def create_html_buttons(tag: Callable[..., Any], text: Callable[[str], None]) -> None:
    # Construct buttons with icons
    buttons = {
        "Directus": {
            "url": "https://emi-collection.unifr.ch/directus",
            "icon": "images/directus.png",
            "css_classes": "directus",
        },
        "NextCloud": {
            "url": "https://emi-collection.unifr.ch/nextcloud",
            "icon": "images/nextcloud.png",
            "css_classes": "nextcloud",
        },
        "QFieldCloud": {
            "url": "https://emi-collection.unifr.ch/qfieldcloud",
            "icon": "images/qfieldcloud.png",
            "css_classes": "qfieldcloud",
        },
    }
    # Button container
    with tag("body"), tag("div", klass="container"):
        with tag("h1"):
            text("Services")

        with tag("div", klass="button-container"):
            for button_name, attributes in buttons.items():
                css_class = attributes.get("css_classes", "")
                combined_class = f"button {css_class}"

                with tag("a", klass=combined_class, href=attributes["url"]):
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


def create_html_projects(tag: Callable[..., Any], text: Callable[[str], None]) -> None:
    # Get report
    report_data = load_json_report()

    # Load directus_data.json to get total sample count
    data_folder = os.getenv("DATA_PATH") or ""
    directus_path = os.path.join(data_folder, "directus_data.json")

    try:
        with open(directus_path, encoding="utf-8") as f:
            directus_data = json.load(f)
    except FileNotFoundError:
        print(f"Warning: {directus_path} not found.")
        directus_data = []

    # Create containers for projects

    for project_name, project_data in report_data.items():
        # Filter directus data for each project
        directus_data_filtered = [row for row in directus_data if row.get("qfield_project") == project_name]
        total_samples_directus = len(directus_data_filtered)

        # Construct each project
        create_html_project_container(tag, text, project_name, project_data, total_samples_directus)


# Generate the HTML for each project
def create_html_project_container(
    tag: Callable[..., Any],
    text: Callable[[str], None],
    project_name: str,
    project_data: dict[str, Any],
    total_samples_directus: int,
) -> None:
    # Create a container for each project
    with tag("div", klass="container"):
        # Create header
        garden_name = utils.get_garden_names_from_qfield_code(project_name)
        create_project_header(tag, text, garden_name, total_samples_directus)

        # Create progressbar
        percentages = project_data.get("percentages", {})
        totals = project_data
        create_project_progressbar(tag, text, percentages, totals)

        # Create details
        create_project_details(tag, text, project_data, project_name)


def create_project_header(
    tag: Callable[..., Any], text: Callable[[str], None], garden_name: str, total_samples_directus: int
) -> None:
    with tag("h2"):
        text(f"Collection status for {garden_name}")

    # Put update date
    with tag("p", klass="small-text"):
        text(f'(Last update on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")})')

    with tag("p", klass="section-subtitle"):
        text("Total of samples collected")
    with tag("div", klass="sample-box"):
        text(f"{total_samples_directus} samples")


def create_project_progressbar(
    tag: Callable[..., Any], text: Callable[[str], None], percentages: dict[str, float], totals: dict[str, int]
) -> None:
    # Get the percentages value
    collected_percent = percentages.get("collected_percent", 0)
    extracted_percent = percentages.get("extracted_percent", 0)
    profiled_percent = percentages.get("profiled_percent", 0)

    # Get total values
    total_available = totals.get("total_available", 0)
    total_collected = totals.get("total_collected", 0)
    total_extracted = totals.get("total_extracted", 0)
    total_profiled = totals.get("total_profiled", 0)

    # Subtitle
    with tag("p", klass="section-subtitle"):
        text("Percentage of species covered in the garden")

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
        # profiled
        with tag("div", klass="legend-item"):
            with tag("span", klass="legend-circle", style="background-color: #00e600;"):
                pass
            with tag("span", klass="legend-text"):
                text(f"{total_profiled} Profiled ({profiled_percent:.1f}%)")

        # extracted
        with tag("div", klass="legend-item"):
            with tag("span", klass="legend-circle", style="background-color: #ffee00;"):
                pass
            with tag("span", klass="legend-text"):
                text(f"{total_extracted} Extracted ({extracted_percent:.1f}%)")

        # collected
        with tag("div", klass="legend-item"):
            with tag("span", klass="legend-circle", style="background-color: #ff9900;"):
                pass
            with tag("span", klass="legend-text"):
                text(f"{total_collected} Collected ({collected_percent:.1f}%)")

        # total
        with tag("div", klass="legend-item"):
            with tag("span", klass="legend-circle", style="background-color: #ffffff;"):
                pass
            with tag("span", klass="legend-text"):
                text(f"{total_available} Total (100%)")


def create_project_details(
    tag: Callable[..., Any], text: Callable[[str], None], project_data: dict[str, Any], project_name: str
) -> None:
    # Details button
    with tag("button", klass="details-button", onclick=f"toggleDetails('details-{project_name}')"):
        text("Details")

    # Details section to be displayed when clicked
    with tag("div", klass="list-container", id=f"details-{project_name}"), tag("h1"):
        # Add to collect list
        create_to_collect_list(tag, text, to_collect_list=project_data.get("to_collect_json", []))

        # Get the unresolved lists
        not_resolved_directus = project_data.get("not_resolved_directus", [])
        not_resolved_botavista = project_data.get("not_resolved_botavista", [])
        no_more_in_garden = project_data.get("no_more_in_garden_json", [])

        # Add different lists
        create_classical_list(
            tag=tag,
            text=text,
            species_list=no_more_in_garden,
            list_name=f"Species collected but no more in the garden ({len(no_more_in_garden)})",
            main_key="resolved_species",
        )
        create_classical_list(
            tag=tag,
            text=text,
            species_list=not_resolved_directus,
            list_name="Unresolved species present in Directus",
            main_key="species",
        )
        create_classical_list(
            tag=tag,
            text=text,
            species_list=not_resolved_botavista,
            list_name="Unresolved species present in Botavista",
            main_key="species",
        )


def create_classical_list(
    tag: Callable[..., Any],
    text: Callable[[str], None],
    species_list: dict[str, Any],
    list_name: str,
    main_key: str = "species",
) -> None:
    with tag("details"):
        with tag("summary", klass="summary-main"):
            text(list_name)
        if species_list:
            with tag("ul"):
                for item in species_list:
                    if isinstance(item, dict):
                        with tag("li"):
                            # Species name
                            with tag("span", klass="plant-name"):
                                text(item.get(main_key, "Unknow species"))
                            # Table with other infos
                            with tag("table", klass="flexible-layout-table"):
                                # Create a single row for keys
                                with tag("tr"):
                                    for key in item:
                                        if key == main_key:
                                            continue
                                        with tag("th"):
                                            text(key)
                                # Create a single row for values
                                with tag("tr"):
                                    for key, value in item.items():
                                        if key == main_key:
                                            continue
                                        with tag("td"):
                                            text(str(value))

                    else:
                        pass
        else:
            with tag("p"):
                text("No species on this list")


def create_to_collect_list(
    tag: Callable[..., Any], text: Callable[[str], None], to_collect_list: list[dict[str, Any]]
) -> None:
    with tag("details", klass="main-details"):
        with tag("summary", klass="summary-main"):
            text("Species to collect")
        with tag("div", klass="to-collect-plants-content"):
            # Sort plants by locations
            locations: dict[str, list[dict[str, Any]]] = {}
            for plant in to_collect_list:
                for location in plant.get("locations", []):
                    if location not in locations:
                        locations[location] = []
                    locations[location].append(plant)
            # Add a details section for each location
            for location, plants in locations.items():
                plant_count = len(plants)
                with tag("details"):
                    with tag("summary"):
                        text(f"{location} ({plant_count} plants)")
                    with tag("ul"):
                        for plant in plants:
                            with tag("li"):
                                text(plant.get("species", "Unknown species"))
                                # Add other infos about the plant
                                with tag("table", klass="fixed-layout-table"):
                                    for key, value in plant.items():
                                        if key == "species" or key == "locations":
                                            continue
                                        with tag("tr"):
                                            with tag("td"):
                                                text(f"{key}:")
                                            with tag("td"):
                                                text(str(value))


def write_html_file(content: str) -> None:
    # Get html folder from .env
    html_folder = os.getenv("HTML_PATH") or ""

    # Create html path
    html_file = os.path.join(html_folder, "home_page.html")

    # Create file
    with open(html_file, "w", encoding="utf-8") as file:
        file.write(content)

    print("Responsive HTML file generated successfully!")


# Generate the homepage
generate_homepage()
