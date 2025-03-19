# generate_html.py
import os
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

# Sample data: Replace with your actual lists
list1 = {"Rose", "Tulip", "Orchid", "Sunflower"}
list2 = {"Tulip", "Orchid", "Lily", "Daisy"}

# Find unique plants
only_in_list1 = list1 - list2
only_in_list2 = list2 - list1

# Get script location
script_location = os.path.abspath(__file__)

# Get the parent directory of the script
parent_directory = os.path.dirname(script_location)

# Generate HTML
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; text-align: center; }}
        h1 {{ color: #2c3e50; }}

        /* List container styling */
        .list-container {{ display: flex; justify-content: space-around; }}
        .list {{ border: 1px solid #ddd; padding: 20px; border-radius: 5px; background: #f9f9f9; }}

        /* Button container styling */
        .button-container {{
            display: flex;
            justify-content: space-between;
            gap: 2%;
            margin-top: 20px;
            flex-wrap: nowrap;  /* Prevent wrapping */
        }}

        /* Styling for individual buttons */
        .btn {{
            flex: 1;  /* Make all buttons the same width */
            padding: 10px 0;
            font-size: 3vw;  /* Responsive font size for icon */
            background-color: #e6e600;
            color: white;
            border: none;
            border-radius: 40px;
            cursor: pointer;
            text-decoration: none;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            transition: background-color 0.3s;
        }}

        .btn:hover {{ background-color: #ffff33; }}

        /* Icon size */
        .btn img, .btn i {{
            width: 12vw;  /* Large icon size relative to viewport width */
            height: 12vw;  /* Maintain square aspect ratio */
            margin-bottom: 5px;  /* Space between icon and text */
        }}

        /* Text size and styling */
        .btn span {{
            font-size: 2vw;  /* Smaller text size relative to viewport width */
            text-transform: capitalize;
        }}

        /* Media query for small screens (e.g., smartphones) */
        @media (max-width: 768px) {{
            .btn {{
                font-size: 6vw;  /* Increase font size for smaller screens */
                padding: 8px 0;
            }}
            .btn img, .btn i {{
                width: 20vw;  /* Increase icon size for smaller screens */
                height: 20vw;
            }}
            .btn span {{
                font-size: 3.5vw;  /* Increase text size on small screens */
            }}
        }}
    </style>
</head>
<body>

    <div class="button-container">
        <a href="https://emi-collection.unifr.ch/directus" class="btn" target="_blank">
            <img src="images/directus.png" alt="Directus Icon" />
            <span>Directus</span>
        </a>
        <a href="https://emi-collection.unifr.ch/nextcloud" class="btn" target="_blank">
            <img src="images/nextcloud.png" alt="NextCloud Icon" />
            <span>NextCloud</span>
        </a>
        <a href="https://emi-collection.unifr.ch/qfieldcloud" class="btn" target="_blank">
            <img src="images/qfieldcloud.png" alt="QFieldCloud Icon" />
            <span>QFieldCloud</span>
        </a>
    </div>

    <h1>Collection status</h1>
    <p>(updated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")})</p>

    <progress id="progress-bar" value="50" max="100"></progress>

    <div class="list-container">
        <div class="list">
            <h2>Only in List 1</h2>
            <ul>
                {"".join(f"<li>{plant}</li>" for plant in only_in_list1)}
            </ul>
        </div>
        <div class="list">
            <h2>Only in List 2</h2>
            <ul>
                {"".join(f"<li>{plant}</li>" for plant in only_in_list2)}
            </ul>
        </div>
    </div>
</body>
</html>"""

data_folder = str(os.getenv("DATA_PATH"))

html_file = os.path.join(data_folder, "home_page.html")

# Save to file
with open(html_file, "w", encoding="utf-8") as file:
    file.write(html_content)

print("HTML file generated: plants_comparison.html")
