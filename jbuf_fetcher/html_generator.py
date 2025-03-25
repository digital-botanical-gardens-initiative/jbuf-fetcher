import json
import os
from datetime import datetime

from dotenv import load_dotenv
from yattag import Doc

load_dotenv()


def generate_homepage(buttons: dict, data_path: str) -> str:
    doc, tag, text, line = Doc().ttl()

    with tag("html"), tag("head"), tag("title"):
        text("Home")

    # Viewport for responsiveness
    with (
        tag("meta", name="viewport", content="width=device-width, initial-scale=1.0"),
        tag(
            "link",
            rel="stylesheet",
            href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",
        ),
        tag("style"),
    ):
        text("""
            /* Global Reset */
            * { margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, sans-serif; text-align: center; }

            /* Centered container */
            .container { width: 100%; margin: 20px auto; padding: 20px; border-radius: 40px; background: #c5cfbf; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); }

            /* Button Container */
            .button-container {
                display: flex;
                justify-content: space-between;
                gap: 2%;
                margin-top: 20px;
                flex-wrap: nowrap;
            }
            .button {
                flex: 1;
                padding: 10px 0;
                font-size: 3vw;
                background-color: #5c7444;
                color: white;
                border: 40px;
                border-radius: 40px;
                cursor: pointer;
                text-decoration: none;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                transition: background-color 0.3s;
            }
            .button:hover { background: #94a58c; }

            /* Icon Styling */
            .button img, .button i {
                width: 5vw;
                height: 5vw;
            }

            .list {
                border: 1px solid #ddd;
                padding: 20px;
                border-radius: 5px;
                background: #f9f9f9;
                text-align: left;
            }

            /* Responsive Design */
            @media (max-width: 1000px) {
                .button { width: 100%; justify-content: center; }
            }

            .progress-container {
                width: 100%;
                height: 30px;
                background-color: #fff;  /* Fond blanc pour toute la zone de progression */
                border-radius: 20px;
                position: relative;
                box-sizing: border-box;
                margin-bottom: 10px; /* Espacement entre les projets */
            }

            .progress-bar {
                height: 100%;
                border-radius: 20px;
                position: absolute;
                top: 0;
            }

            /* Specific color for each status*/
            .collected {
                background-color: #244c0c;
                height: 30px;
            }

            .extracted {
                background-color: #4f6b3a;
                height: 25px;
            }

            .profiled {
                background-color: #718964;
                height: 20px;
            }

            .small-text {
                font-size: 15px;
                color: #888;
                margin-bottom: 15px;
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
            text("Collection status ")
            text(i.upper())
            with tag("p", klass="small-text"):
                text(f'(Last update on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")})')

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

# Get data folder
data_path = str(os.getenv("DATA_PATH"))

# Check that data folder exists
if not data_path:
    print("Error : no DATA_PATH")
    exit(1)

# Create html path
html_file = os.path.join(data_path, "home_page.html")

# Generate HTML and save to file
html_content = generate_homepage(buttons, data_path)
with open(html_file, "w") as file:
    file.write(html_content)

print("Responsive HTML file generated successfully!")
