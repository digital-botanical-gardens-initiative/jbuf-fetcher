import os

import pandas as pd
from dotenv import load_dotenv
import requests

load_dotenv()

json_path = os.path.join(os.getenv("DATA_PATH"), "directus_data.json")

df = pd.read_json(json_path)

session = requests.Session()

url = "https://finder.globalnames.org/api/v1/find"

# name = 'Echeveria elegans'
# payload = {
#     "text": name,
#     "format": "json",
#     "bytesOffset": False,
#     "returnContent": True,
#     "uniqueNames": True,
#     "ambiguousNames": False,
#     "noBayes": False,
#     "oddsDetails": False,
#     "language": "eng",
#     "wordsAround": 0,
#     "verification": True,
#     "sources": [
#         1,
#         12,
#         169
#     ],
#     "allMatches": False
# }
# response = session.post(url, json=payload)
# print(response.json())

fail_counter = 0

for index, row in df.iterrows():
    name = str(row["sample_name"]).capitalize()
    if name == "aaunknown" or name == "None" or name == "Aaunknown": # TODO: Once Heloïse has a clean json, remove this
        continue

    payload = {
        "text": name,
        "format": "json",
        "bytesOffset": False,
        "returnContent": True,
        "uniqueNames": True,
        "ambiguousNames": False,
        "noBayes": False,
        "oddsDetails": False,
        "language": "eng",
        "wordsAround": 0,
        "verification": True,
        "sources": [
            1,
            12,
            169
        ],
        "allMatches": False
    }
    response = session.post(url, json=payload)
    if response.status_code == 200:
        if (response.json()["names"] != [] and response.json()["names"] != None):
            matched_name = response.json()["names"][0]["verification"]["bestResult"]["currentCanonicalSimple"]
            if matched_name == "":
                matched_name = response.json()["names"][0]["verification"]["bestResult"]["matchedCanonicalSimple"]
                if matched_name == "":
                    print("Resolved but no match")
                    print(response.json()["names"][0])
            #print(f"raw name: {name}")
            #print(f"resolved name: {matched_name}")
        else:
            payload = {
                "text": name,
                "format": "json",
                "bytesOffset": False,
                "returnContent": True,
                "uniqueNames": True,
                "ambiguousNames": True,
                "noBayes": False,
                "oddsDetails": False,
                "language": "eng",
                "wordsAround": 0,
                "verification": False,
                "sources": [
                    1,
                    12,
                    169
                ],
                "allMatches": False
            }
            response = session.post(url, json=payload)
            if response.status_code == 200:
                if (response.json()["names"] != [] and response.json()["names"] != None):
                    matched_name = response.json()["names"][0]["verification"]["bestResult"]["currentCanonicalSimple"]
                    if matched_name == "":
                        matched_name = response.json()["names"][0]["verification"]["bestResult"]["matchedCanonicalSimple"]
                        if matched_name == "":
                            print("Resolved but no match")
                            print(response.json()["names"][0])
                else:
                    fail_counter += 1
                    matched_name = None
                    print("Not resolved")
                    print(response.json())
    else:
        print("Connection to gnames failed.")
print(fail_counter)
