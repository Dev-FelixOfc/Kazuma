import json
import os

JSON_PATH = os.path.join(os.path.dirname(__file__), "../../config.json")

def get_json_data():
    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, "r") as f:
            return json.load(f)
    return {}

json_data = get_json_data()

CONFIG = {
    "bot_name": "Kazuma",
    "owner": "5350045157",
    "prefix": "/",
    "phone_number": json_data.get("phone_number", ""),
    "password": json_data.get("password", "")
}