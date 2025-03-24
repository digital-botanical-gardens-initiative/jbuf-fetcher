import os

from dotenv import load_dotenv
from yattag import Doc

load_dotenv()


def generate_homepage(buttons: dict) -> str:
    doc, tag, text = Doc().tagtext()

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
            .container { width: 100%; margin: 20px auto; padding: 20px; border-radius: 10px; background: #f8f9fa; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); }

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
                background-color: #e6e600;
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
            .button:hover { background: #ffff66; }

            /* Icon Styling */
            .button img, .button i {
                width: 5vw;
                height: 5vw;
            }

            /* Responsive Design */
            @media (max-width: 1000px) {
                .button { width: 100%; justify-content: center; }
            }
            """)

    with tag("body"), tag("div", klass="container"):
        with tag("h1"):
            text("Services")

        # Button container
        with tag("div", klass="button-container"):
            for button_name, attributes in buttons.items():
                print(f"name: {button_name}, attributes; {attributes}")
                with tag("a", klass="button", href=attributes["url"]):
                    with tag("img", src=attributes["icon"]):  # Add icon
                        pass
                    text(button_name)  # Button text

    return doc.getvalue()


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

# Get data
resolved_data = os.path.join(data_path, "resolved_data.json")
not_resolved_data = os.path.join(data_path, "not_resolved_data.json")

# Create html path
html_file = os.path.join(data_path, "home_page.html")

# Generate HTML and save to file
html_content = generate_homepage(buttons)
with open(html_file, "w") as file:
    file.write(html_content)

print("Responsive HTML file generated successfully!")
