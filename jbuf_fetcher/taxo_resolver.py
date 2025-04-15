import json
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

data_path = str(os.getenv("DATA_PATH"))

json_path_directus = os.path.join(data_path, "directus_data.json")
json_path_botavista = os.path.join(data_path, "botavista_data.json")

with open(json_path_directus, encoding="utf-8") as f:
    data_directus = json.load(f)

with open(json_path_botavista, encoding="utf-8") as f:
    data_botavista = json.load(f)

session = requests.Session()

url = "https://finder.globalnames.org/api/v1/find"


def clean_species_name(raw_name: str) -> str:
    # Clean and format the species name
    name = raw_name.replace("_", " ")  # Get name and replace underscores by white spaces
    name = re.sub(r"[^a-zA-Z ]", "", name).strip()  # Remove all non alphabetical characters
    name = re.sub(r"\s+", " ", name)  # Remove multiple spaces
    words = name.split(" ")
    if words and len(words[0]) < 3:  # Remove first part if shorter than 3 characters
        words.pop(0)
    return " ".join(words).capitalize()


def is_excluadable_name(name: str) -> bool:
    # Check if the name should be excluded from resolution (skip unknow or malformed names)
    return name in ["None", "Aaunknown", "Unknown"] or len(name.split(" ")) < 2


def build_payload(name: str) -> dict[str, Any]:
    # Create the payload for the resolution API
    return {
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
        "verification": True,
        "sources": [1, 12, 169],
        "allMatches": True,
    }


def parse_resolution_response(name: str, resp_json: dict[str, Any], obj: dict[str, Any]) -> tuple[dict[str, Any], bool]:
    # Interpret the API response and update the object accordingly
    try:
        verification = resp_json["names"][0]["verification"]
        if not verification.get("bestResult"):
            matched_name = verification.get("name")
            obj.update({
                "submitted_name": name,
                "resolution_confidence": "low",
                "resolved_species": matched_name,
            })
            return obj, True
        else:
            best_result = verification["bestResult"]
            matched_name = best_result.get("currentCanonicalSimple") or best_result.get("matchedCanonicalSimple")
            confidence = "high" if best_result.get("currentCanonicalSimple") else "medium"
            obj.update({
                "submitted_name": name,
                "resolution_confidence": confidence,
                "resolved_species": matched_name,
            })
            return obj, True
    except Exception as e:
        obj["submitted_name"] = name
        obj["resolution_error"] = f"Error: Couldn't extract result - {e} - Response: {resp_json}"
        return obj, False


def resolve_name(obj: dict[str, Any]) -> tuple[dict[str, Any], bool]:
    # Resolve scientific name and return modified JSON object.
    raw_name = str(obj.get("species", ""))
    cleaned_name = clean_species_name(raw_name)

    if is_excluadable_name(cleaned_name):
        obj["submitted_name"] = cleaned_name
        obj["resolution_error"] = "Excluded"
        return obj, False

    payload = build_payload(cleaned_name)

    try:
        response = session.post(url, json=payload)
        if response.status_code == 200:
            return parse_resolution_response(cleaned_name, response.json(), obj)
        else:
            obj["submitted_name"] = cleaned_name
            obj["resolution_error"] = f"Error: Bad - Code: {response.status_code} - Message: {response.text}"
            return obj, False
    except requests.RequestException as e:
        obj["submitted_name"] = cleaned_name
        obj["resolution_error"] = f"Error: Request failed - {e}"
        return obj, False


def batch_run(data: dict, collection: str, max_retries: int = 5) -> None:
    # Parallel processing using ThreadPoolExecutor
    resolved_results = []
    error_results = []
    excluded_results = []

    to_retry = [{"obj": obj, "retries": 0} for obj in data]

    while to_retry:
        next_round = []

        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_data = {executor.submit(resolve_name, item["obj"]): item for item in to_retry}

            for future in as_completed(future_to_data):
                item = future_to_data[future]

                try:
                    result, success = future.result()
                    resolution_error = result.get("resolution_error", "")
                    if resolution_error == "Excluded":
                        excluded_results.append(result)
                        continue

                    if success:
                        resolved_results.append(result)
                    else:
                        if item["retries"] + 1 < max_retries:
                            next_round.append({"obj": result, "retries": item["retries"] + 1})
                        else:
                            error_results.append(result)
                except Exception as e:
                    item["obj"]["resolution_error"] = f"Unexpected Error during retry: {e}"
                    error_results.append(item["obj"])

        to_retry = next_round

    data_file = os.path.join(data_path, f"resolved_data_{collection}.json")
    error_file = os.path.join(data_path, f"not_resolved_data_{collection}.json")
    excluded_file = os.path.join(data_path, f"excluded_data_{collection}.json")

    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(resolved_results, f, indent=4, ensure_ascii=False)

    with open(error_file, "w", encoding="utf-8") as f:
        json.dump(error_results, f, indent=4, ensure_ascii=False)

    with open(excluded_file, "w", encoding="utf-8") as f:
        json.dump(excluded_results, f, indent=4, ensure_ascii=False)

    print(
        f"Resolved data saved to {data_file}, unresolved data saved to {error_file}, Excluded data saved to {excluded_file}"
    )


batch_run(data_directus, "directus")
batch_run(data_botavista, "botavista")
