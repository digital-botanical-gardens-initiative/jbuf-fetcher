import os
import json
from dotenv import load_dotenv

load_dotenv()

# Get the data lists 
data_folder = os.getenv("DATA_PATH")
file_path = os.path.join(data_folder, "resolved_data_directus.json")

if os.path.exists(file_path):
    print("test")
# Split the data lists by projects 

# for each project : 

    # Compare botavista and directus 

    # Get the collected % 

    # Compare botavista and directus "extracted = true"

    # Get the extracted % 

    # Compare botavista and directus "profiled = true"

    # Get the profiled %


# Create a json with [project, % collected, % extracted, % profiled] (will be use in html_generator)