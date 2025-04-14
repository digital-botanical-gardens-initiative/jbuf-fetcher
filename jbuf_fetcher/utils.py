import json
import os


# Load dictonary for project name
def load_project_mappings() -> list[dict[str, str]]:
    # Path to the JSON file
    data_path = os.getenv("DATA_PATH", "")
    mappings_file = os.path.join(data_path, "project_mappings.json")

    # Load the JSON file
    try:
        with open(mappings_file, encoding="utf-8") as file:
            # Load the entire JSON structure
            data: list[dict[str, str]] = json.load(file)
            # Ensure the data is a dictionary with the expected structure
            # Ensure the data is not empty
            if len(data) == 0:
                print(f"Error: The mappings file '{mappings_file}' is empty.")
                exit()
            return data
    except FileNotFoundError:
        print(f"Error: The mappings file '{mappings_file}' does not exist.")
        exit()
    except json.JSONDecodeError:
        print(f"Error: Unable to decode JSON file '{mappings_file}'.")
        exit()


def get_qfield_codes() -> list[str]:
    # Load project mappings
    projects = load_project_mappings()

    qfield_codes: list[str] = []

    for project in projects:
        code = project.get("qfield_code", None)
        if code is None:
            print(f"Error: Missing qfield code in {project}.")
            exit()

        qfield_codes.append(code)

    return qfield_codes


def get_botavista_codes() -> list[str]:
    # Load project mappings
    projects = load_project_mappings()

    botavista_codes: list[str] = []

    for project in projects:
        code = project.get("botavista_code", None)
        if code is None:
            print(f"Error: Missing botavista code in {project}.")
            exit()
        botavista_codes.append(code)

    return botavista_codes


def get_garden_names() -> list[str]:
    # Load project mappings
    projects = load_project_mappings()

    garden_names: list[str] = []

    for project in projects:
        name = project.get("garden_name", None)
        if name is None:
            print(f"Error: Missing garden name in {project}.")
            exit()

        garden_names.append(name)

    return garden_names


def get_qfield_code_from_botavista_code(botavista_code: str) -> str:
    # Load project mappings
    projects = load_project_mappings()

    for project in projects:
        if project["botavista_code"] == botavista_code:
            return project["qfield_code"]

    print(f"Error: Botavista code {botavista_code} not found in project mappings.")
    exit()


def get_garden_names_from_qfield_code(qfield_code: str) -> str:
    # Load project mappings
    projects = load_project_mappings()

    for project in projects:
        if project["qfield_code"] == qfield_code:
            return project["garden_name"]
    print(f"Error: Qfield code {qfield_code} not found in project mappings.")
    exit()
