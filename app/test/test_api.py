import requests
import json
import os

url = "http://localhost:8000/api/generate-heatmap"

base_path = os.path.dirname(os.path.abspath(__file__))
full_dir = os.path.join(base_path, "test_request.json")

with open(full_dir, "r") as file:
    payload = json.load(file)

with open(os.path.join(base_path, payload["data_json_path"]), 'r') as f:
    payload["data_json"] = json.load(f)

del payload["data_json_path"]

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())
