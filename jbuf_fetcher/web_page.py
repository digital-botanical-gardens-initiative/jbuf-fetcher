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
    <title>EMI collection home page</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; text-align: center; }}
        h1 {{ color: #2c3e50; }}
        .list-container {{ display: flex; justify-content: space-around; }}
        .list {{ border: 1px solid #ddd; padding: 20px; border-radius: 5px; background: #f9f9f9; }}
        .button-container {{ display: flex; justify-content: center; gap: 20px; margin-top: 20px; }}
        .btn {{ padding: 10px 20px; font-size: 25px; background-color: #cccc00; color: white; border: none; border-radius: 30px; cursor: pointer; text-decoration: none; display: inline-flex; align-items: center; }}
        .btn:hover {{ background-color: #ff9966; }}
        .btn img {{ width: 100px; height: 100px; margin-right: 8px; }}
    </style>
</head>
<body>

    <div class="button-container">
        <a href="https://emi-collection.unifr.ch/directus" class="btn" target="_blank">
            <img src="../images/directus.png" alt="Directus Icon" /> Directus
        </a>
        <a href="https://emi-collection.unifr.ch/nextcloud" class="btn" target="_blank">
            <img src="../images/nextcloud.png" alt="NextCloud Icon" /> NextCloud
        </a>
        <a href="https://emi-collection.unifr.ch/qfieldcloud" class="btn" target="_blank">
            <img src="../images/qfieldcloud.png" alt="QFieldCloud Icon" /> QFieldCloud
        </a>
    </div>

    <h1>Collection status (updated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")})</h1>

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
