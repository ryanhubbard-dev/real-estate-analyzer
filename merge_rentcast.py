
import json
from pathlib import Path

data_dir = Path("data")

page1_path = data_dir / "rentcast_properties_greenridge_1mi.json"
page2_path = data_dir / "rentcast_properties_greenridge_1mi_page2.json"
output_path = data_dir / "rentcast_properties_merged.json"

with page1_path.open("r", encoding="utf-8") as file:
    page1 = json.load(file)

with page2_path.open("r", encoding="utf-8") as file:
    page2 = json.load(file)

all_properties = page1 + page2

unique_properties = {}

for property_data in all_properties:
    property_id = property_data["id"]
    unique_properties[property_id] = property_data

merged_properties = list(unique_properties.values())

print("\nRENTCAST MERGE REPORT")
print("-" * 50)
print(f"Page 1 records: {len(page1)}")
print(f"Page 2 records: {len(page2)}")
print(f"Combined records: {len(all_properties)}")
print(f"Unique properties: {len(merged_properties)}")
print(f"Duplicates: {len(all_properties) - len(merged_properties)}")

with output_path.open("w", encoding="utf-8") as file:
    json.dump(merged_properties, file, indent=2)

print(f"\nSaved merged dataset to {output_path}")
