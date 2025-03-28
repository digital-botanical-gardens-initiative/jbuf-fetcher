# generate_html.py
import json
import os
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

# Get the json list
not_resolved_data_path = os.getenv("DATA_PATH")
if not not_resolved_data_path:
    print("Error : no DATA_PATH")
    exit(1)

json_path = os.path.join(not_resolved_data_path, "not_resolved_data.json")

# Sample data: Replace with your actual lists
list1 = {"Rose", "Tulip", "Orchid", "Sunflower", "Bellis", "Muguet"}
list2 = {"Tulip", "Orchid", "Lily", "Daisy", "Jonquille"}

# Find unique plants
only_in_list1 = list1 - list2
only_in_list2 = list2 - list1

# Collection variables
percentage_collect_fribourg = 65
percentage_collect_neuchatel = 35
percentage_extraction_fribourg = 50
percentage_extraction_neuchatel = 20

# Variables for multiple progress bar
profiled_fr = 25
extracted_fr = 40
collected_fr = 60
profiled_ne = 20
extracted_ne = 20
collected_ne = 50

# Generate the list
with open(json_path, encoding="utf-8") as f:
    data = json.load(f)

not_resolved_data_html = "<ul>\n"
for item in data:
    not_resolved_data_html += "    <li>\n"
    for key, value in item.items():
        not_resolved_data_html += f"        <strong>{key}:</strong> {value}<br>\n"
    not_resolved_data_html += "    </li>\n"
not_resolved_data_html += "</ul>\n"


# Generate HTML
html_style = """<!DOCTYPE html>
<html lang="en">
 <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            text-align: center;
        }
        h1 {
            margin-top: 50px;
            color: #2c3e50;
        }

        /* List container styling */
        .list-container {
            display: flex;
            justify-content: space-around;
        }
        .list {
            border: 1px solid #ddd;
            padding: 20px;
            border-radius: 5px;
            background: #f9f9f9;
            text-align: left;
        }

        /* Button container styling */
        .button-container {
            display: flex;
            justify-content: space-between;
            gap: 2%;
            margin-top: 20px;
            flex-wrap: nowrap;
        }

        /* Styling for individual buttons */
        .btn {
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

        .btn:hover {
            background-color: #ffff33;
        }

        /* Icon size */
        .btn img, .btn i {
            width: 12vw;
            height: 12vw;
            margin-bottom: 5px;
        }

        /* Text size and styling */
        .btn span {
            font-size: 2vw;
            text-transform: capitalize;
        }

        /* Styling for the jbuf container */
        .bg-container {
            display: flex;  /* Use flexbox to align children horizontally */
            align-items: center;  /* Vertically align items in the center */
            justify-content: space-between;  /* Align h1 to the left and progress bar to the right */
            width: 100%;
            margin-botom: 50px;
        }

        /* Optional: Make the title smaller or adjust its font size */
        .bg-container h1 {
            font-size: 1.5em;  /* Adjust size of the title */
            margin: 0;  /* Remove any default margin */
            width: 40%
        }

        /* Progress bar styling */
        #progress-bar {
            width: 60%;
            height: 50px;
            border-radius: 40px;
            border: 5px solid #2c3e50;
            margin: 20px auto;
            background-color: #f2f2f2;
        }

        #progress-bar::-webkit-progress-bar {
            border-radius: 40px;
            background-color: #f2f2f2;
        }

        #progress-bar::-webkit-progress-value {
            border-radius: 40px;
            background: #00e64d
        }

        /* Firefox */
        #progress-bar::-moz-progress-bar {
            border-radius: 40px;
            background: #00e64d
        }

        /* Media query for small screens */
        @media (max-width: 768px) {
            .btn {
                font-size: 6vw;
                padding: 8px 0;
            }
            .btn img, .btn i {
                width: 20vw;
                height: 20vw;
            }
            .btn span {
                font-size: 3.5vw;
            }
            #progress-bar {
                width: 90%;
                height: 25px;
            }
        }
        table {
            width: 90%;
            margin: auto;
            border-collapse: collapse;
            table-layout: fixed;
        }
        td {
            border: 1px solid black;
            padding: 8px;
            text-align: center;
            vertical-align: middle;
            width: 25%; /* Width of each column */
            word-wrap: break-word;
            overflow-wrap: break-word; /* Cut words properly */
            white-space: normal;
        }
    </style>
    """

html_content_home = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
    {html_style}
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">

</head>
<body>

    <h1>Access services</h1>

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
    </div>"""

html_content_fr = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
    {html_style}
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">


    <h1>Collection status</h1>
    <p>(updated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")})</p>

</head>
<body>
<head>

  <title>Bootstrap Progress Bars</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <link href="https://fonts.googleapis.com/css?family=Amatic+SC" rel="stylesheet">


  <div class="container">
    <h2>Jardin Botanique de l'Université de Fribourg</h2>
    <p>Status of our samples</p>
      <div class="progress">
        <div class="progress-bar progress-bar-success" role="progressbar" aria-valuenow="95" aria-valuemin="0" aria-valuemax="100" style="width:{collected_fr}%">Collected
        </div>
      </div>
      <div class="progress">
        <div class="progress-bar progress-bar-info" role="progressbar" aria-valuenow="90" aria-valuemin="0" aria-valuemax="100" style="width:{extracted_fr}%">Extracted
        </div>
      </div>
      <div class="progress">
        <div class="progress-bar progress-bar-warning" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style="width:{profiled_fr}%">Profiled
        </div>
      </div>


  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Not resolved data</title>
  {html_style}
<head>
  <h1>Not resolved data</h1>
  <div class="list-container">
    {not_resolved_data_html}
  </div>
</body>
    """


html_content_ne = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
    {html_style}


<head>

  <title>Bootstrap Progress Bars</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <link href="https://fonts.googleapis.com/css?family=Amatic+SC" rel="stylesheet">



  <div class="container">
    <h2>Jardin Botanique de l'Université de Neuchatel</h2>
    <p>Status of the samples</p>
      <div class="progress">
        <div class="progress-bar progress-bar-success" role="progressbar" aria-valuenow="95" aria-valuemin="0" aria-valuemax="100" style="width:{collected_ne}%">Collected
        </div>
      </div>
      <div class="progress">
        <div class="progress-bar progress-bar-info" role="progressbar" aria-valuenow="90" aria-valuemin="0" aria-valuemax="100" style="width:{extracted_ne}%">Extracted
        </div>
      </div>
      <div class="progress">
        <div class="progress-bar progress-bar-warning" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style="width:{profiled_ne}%">Profiled
        </div>
      </div>


</html>"""

data_folder = str(os.getenv("DATA_PATH"))

html_file = os.path.join(data_folder, "home_page.html")

# Merge all html file
html_full = html_style + html_content_home + html_content_fr + html_content_ne

# Save to file
with open(html_file, "w", encoding="utf-8") as file:
    file.write(html_full)

print("HTML file successfully generated")
