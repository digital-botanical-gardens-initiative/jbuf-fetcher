# generate_html.py
import os
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

# Sample data: Replace with your actual lists
list1 = {"Rose", "Tulip", "Orchid", "Sunflower", "Bellis", "Muguet"}
list2 = {"Tulip", "Orchid", "Lily", "Daisy", "Jonquille"}

# Find unique plants
only_in_list1 = list1 - list2
only_in_list2 = list2 - list1

percentage_collect_fribourg = 65
percentage_collect_neuchatel = 35
percentage_extraction_fribourg = 50
percentage_extraction_neuchatel = 20

# Variables for stack bar
profiled = 20
extracted = 20
collected = 50

# Generate HTML
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            text-align: center;
        }}
        h1 {{
            margin-top: 50px;
            color: #2c3e50;
        }}

        /* List container styling */
        .list-container {{
            display: flex;
            justify-content: space-around;
        }}
        .list {{
            border: 1px solid #ddd;
            padding: 20px;
            border-radius: 5px;
            background: #f9f9f9;
        }}

        /* Button container styling */
        .button-container {{
            display: flex;
            justify-content: space-between;
            gap: 2%;
            margin-top: 20px;
            flex-wrap: nowrap;
        }}

        /* Styling for individual buttons */
        .btn {{
            flex: 1;
            padding: 10px 0;
            font-size: 3vw;
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

        .btn:hover {{
            background-color: #ffff33;
        }}

        /* Icon size */
        .btn img, .btn i {{
            width: 12vw;
            height: 12vw;
            margin-bottom: 5px;
        }}

        /* Text size and styling */
        .btn span {{
            font-size: 2vw;
            text-transform: capitalize;
        }}

        /* Styling for the jbuf container */
        .bg-container {{
            display: flex;  /* Use flexbox to align children horizontally */
            align-items: center;  /* Vertically align items in the center */
            justify-content: space-between;  /* Align h1 to the left and progress bar to the right */
            width: 100%;
            margin-botom: 50px;
        }}

        /* Optional: Make the title smaller or adjust its font size */
        .bg-container h1 {{
            font-size: 1.5em;  /* Adjust size of the title */
            margin: 0;  /* Remove any default margin */
            width: 40%
        }}

        /* Progress bar styling */
        #progress-bar {{
            width: 60%;
            height: 50px;
            border-radius: 40px;
            border: 5px solid #2c3e50;
            margin: 20px auto;
            background-color: #f2f2f2;
        }}

        #progress-bar::-webkit-progress-bar {{
            border-radius: 40px;
            background-color: #f2f2f2;
        }}

        #progress-bar::-webkit-progress-value {{
            border-radius: 40px;
            background: #00e64d
        }}

        /* Firefox */
        #progress-bar::-moz-progress-bar {{
            border-radius: 40px;
            background: #00e64d
        }}

        /* Media query for small screens */
        @media (max-width: 768px) {{
            .btn {{
                font-size: 6vw;
                padding: 8px 0;
            }}
            .btn img, .btn i {{
                width: 20vw;
                height: 20vw;
            }}
            .btn span {{
                font-size: 3.5vw;
            }}
            #progress-bar {{
                width: 90%;
                height: 25px;
            }}
        }}
    </style>
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
    </div>

    <h1>Collection status</h1>
    <p>(updated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")})</p>

    <div class="bg-container">
        <h1>Jardin Botanique de l'Université de Fribourg ({percentage_collect_fribourg}%):</h1>
        <progress id="progress-bar" value={percentage_collect_fribourg} max="100"></progress>
    </div>

    <div class="bg-container">
        <h1>Jardin Botanique de Neuchâtel ({percentage_collect_neuchatel}%):</h1>
        <progress id="progress-bar" value={percentage_collect_neuchatel} max="100"></progress>
    </div>


    <div class="container">
  <h2>Status</h2>
  <p>Status of our samples</p>
  <div class="progress">
    <div class="progress-bar progress-bar-success" role="progressbar" style="width:{profiled}%">
      Profiled
    </div>
    <div class="progress-bar progress-bar-warning" role="progressbar" style="width:{extracted}%">
      Extracted
    </div>
    <div class="progress-bar progress-bar-danger" role="progressbar" style="width:{collected}%">
      Collected
    </div>
  </div>
</div>

<head>

  <title>Bootstrap Progress Bars</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <link href="https://fonts.googleapis.com/css?family=Amatic+SC" rel="stylesheet">

</head>
<body>

</head>
<body>

  <div class="container">
    <h2>My Satus of our samples</h2>
      <div class="progress">
        <div class="progress-bar progress-bar-success" role="progressbar" aria-valuenow="95" aria-valuemin="0" aria-valuemax="100" style="width:{collected}%">Collected
        </div>
      </div>
      <div class="progress">
        <div class="progress-bar progress-bar-info" role="progressbar" aria-valuenow="90" aria-valuemin="0" aria-valuemax="100" style="width:{extracted}%">Extracted
        </div>
      </div>
      <div class="progress">
        <div class="progress-bar progress-bar-warning" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style="width:{profiled}%">Profiled
        </div>
      </div>

</body>

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

<head>
  <title>Bootstrap Example</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
</head>
<body>


</html>"""

data_folder = str(os.getenv("DATA_PATH"))

html_file = os.path.join(data_folder, "home_page.html")

# Save to file
with open(html_file, "w", encoding="utf-8") as file:
    file.write(html_content)

print("HTML file generated: plants_comparison.html")
