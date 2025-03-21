import json
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

data_path = str(os.getenv("DATA_PATH"))

json_path = os.path.join(data_path, "directus_data.json")

with open(json_path, encoding="utf-8") as f:
    data = json.load(f)

session = requests.Session()

url = "https://finder.globalnames.org/api/v1/find"


def resolve_name(obj: dict[str, Any]) -> tuple[dict[str, Any], bool]:
    """Resolve scientific name and return modified JSON object."""
    # Get name and replace underscores by white spaces
    raw_name = str(obj.get("sample_name", "")).replace("_", " ")

    # Remove all non alphabetical characters
    alphabetical_name = re.sub(r"[^a-zA-Z ]", "", raw_name).strip()

    # Remove multiple spaces
    unspaced_name = re.sub(r"\s+", " ", alphabetical_name).strip()

    # Remove first part if shorter than 3 characters
    words = unspaced_name.split(" ")
    if words and len(words[0]) < 3:
        words.pop(0)
    unprefixed_name = " ".join(words)

    # Capitalize name
    cleaned_name = str(unprefixed_name).capitalize()

    # Skip unknown or malformed names
    if cleaned_name in ["None", "Aaunknown", "Unknown"] or len(cleaned_name.split(" ")) < 2:
        obj["submitted_name"] = cleaned_name
        obj["resolution_error"] = "Excluded"
        return obj, False

    # Build json request
    payload = {
        "text": cleaned_name,
        "format": "json",
        "bytesOffset": False,
        "returnContent": True,
        "uniqueNames": True,
        "ambiguousNames": True,
        "noBayes": False,
        "oddsDetails": False,
        "language": "eng",
        "wordsAround": 0,
        "verification": True,
        "sources": [1, 12, 169],
        "allMatches": True,
    }

    # Make request
    try:
        response = session.post(url, json=payload)
        # Check for valid response
        if response.status_code == 200:
            # Store json response
            json_resp = response.json()
            # Check that needed data exist in the json
            try:
                # If bestResult is not present
                if (
                    json_resp.get("names")
                    and json_resp["names"]
                    and json_resp["names"][0].get("verification")
                    and not json_resp["names"][0]["verification"].get("bestResult")
                ):
                    verification = json_resp["names"][0]["verification"]
                    matched_name = verification.get("name")
                    obj["submitted_name"] = cleaned_name
                    obj["resolution_confidence"] = "low"
                    obj["resolved_sample_name"] = matched_name
                    return obj, True
                # If bestResult is present
                elif (
                    json_resp["names"]
                    and json_resp["names"][0]["verification"]
                    and json_resp["names"][0]["verification"]["bestResult"]
                ):
                    best_result = json_resp["names"][0]["verification"]["bestResult"]
                    if best_result.get("currentCanonicalSimple"):
                        matched_name = best_result.get("currentCanonicalSimple")
                        confidence = "high"
                    else:
                        matched_name = best_result.get("matchedCanonicalSimple")
                        confidence = "medium"
                    obj["submitted_name"] = cleaned_name
                    obj["resolution_confidence"] = confidence
                    obj["resolved_sample_name"] = matched_name
                    return obj, True
                else:
                    obj["submitted_name"] = cleaned_name
                    obj["resolution_error"] = f"Error: names or verification doesn't exist - Response: {json_resp}"
                    return obj, False
            except Exception as e:
                obj["submitted_name"] = cleaned_name
                obj["resolution_error"] = f"Error: Couldn't extract result - {e} - Response: {json_resp}"
                return obj, False
        else:
            obj["submitted_name"] = cleaned_name
            obj["resolution_error"] = f"Error: Bad response - Code: {response.status_code} - Message: {response.text}"
            return obj, False
    except requests.RequestException as e:
        obj["submitted_name"] = cleaned_name
        obj["resolution_error"] = f"Error: Request failed - {e}"
        return obj, False


# Parallel processing using ThreadPoolExecutor
resolved_results = []
error_results = []
excluded_results = []

with ThreadPoolExecutor(max_workers=5) as executor:
    future_to_obj = {executor.submit(resolve_name, obj): obj for obj in data}
    for future in as_completed(future_to_obj):
        result, success = future.result()
        if success:
            resolved_results.append(result)
        else:
            if result.get("resolution_error", "") == "Excluded":
                excluded_results.append(result)
            else:
                error_results.append(result)

data_file = os.path.join(data_path, "resolved_data.json")
error_file = os.path.join(data_path, "not_resolved_data.json")
excluded_file = os.path.join(data_path, "excluded_data.json")

with open(data_file, "w", encoding="utf-8") as f:
    json.dump(resolved_results, f, indent=4, ensure_ascii=False)

with open(error_file, "w", encoding="utf-8") as f:
    json.dump(error_results, f, indent=4, ensure_ascii=False)

with open(excluded_file, "w", encoding="utf-8") as f:
    json.dump(excluded_results, f, indent=4, ensure_ascii=False)

print(
    f"Resolved data saved to {data_file}, unresolved data saved to {error_file}, Excluded data saved to {excluded_file}"
)
