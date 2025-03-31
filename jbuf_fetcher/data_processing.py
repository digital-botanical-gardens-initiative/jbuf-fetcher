import os
import json
from dotenv import load_dotenv

load_dotenv()

# Get the data lists
data_folder = os.getenv("DATA_PATH") or ""
file_path_directus = os.path.join(data_folder, "resolved_data_directus.json")
file_path_botavista = os.path.join(data_folder, "resolved_data_botavista.json")

def load_json(file_path, label):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        print(f"{label} successfully charged")
        return data
    else:
        print(f"Error : the file {file_path} does not exist")
        return None
    
data_botavista = load_json(file_path_botavista, "Botavista")
data_directus = load_json(file_path_directus, "Directus")

print(f" Botavista Data : {data_botavista[:2] if data_botavista else 'not charged'}")
print(f" Directus Data : {data_directus[:2] if data_directus else 'not charged'}")
# Split the data lists by projects

# for each project :

# Compare botavista and directus

# Get the collected %

# Compare botavista and directus "extracted = true"

# Get the extracted %

# Compare botavista and directus "profiled = true"

# Get the profiled %


# Create a json with [project, % collected, % extracted, % profiled] and json not_resolved_data (will be use in html_generator)
