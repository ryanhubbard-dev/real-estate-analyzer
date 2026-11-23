
import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("RENTCAST_API_KEY")

if not api_key:
    raise RuntimeError("RentCast API key not found in environment.")

url = "https://api.rentcast.io/v1/properties"

params = {
    "address": "60 Greenridge Ln, Coldspring, TX 77331",
    "radius": 1,
    "propertyType": "Single Family",
    "limit": 500,
    "offset": 500,
    "includeTotalCount": "true",
}

print("\nRENTCAST REQUEST")
print("-" * 50)
print(f"Search center: {params['address']}")
print(f"Radius: {params['radius']} mile(s)")
print(f"Property type: {params['propertyType']}")
print(f"Maximum records: {params['limit']}")
print(f"Starting offset: {params['offset']}")

confirmation = input("\nProceed with API request? (y/n): ")

if confirmation.strip().lower() != "y":
    raise SystemExit("Request cancelled.")

response = requests.get(
    url,
    headers={
        "Accept": "application/json",
        "X-Api-Key": api_key,
    },
    params=params,
    timeout=30,
)

response.raise_for_status()
print("Total matching records:", response.headers.get("X-Total-Count", "Not provided"))
properties = response.json()

data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

output_file = data_dir / "rentcast_properties_greenridge_1mi_page2.json"

if output_file.exists():
    raise FileExistsError(
        f"{output_file} already exists. Refusing to overwrite local data."
    )

with output_file.open("w", encoding="utf-8") as file:
    json.dump(properties, file, indent=2)

print(f"Retrieved {len(properties)} properties.")
print(f"Saved data to {output_file}")
