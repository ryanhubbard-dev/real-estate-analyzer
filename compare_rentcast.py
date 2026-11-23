import json
from pathlib import Path

data_dir = Path("data")

with (data_dir / "rentcast_properties.json").open(encoding="utf-8") as file:
    original = json.load(file)

with (data_dir / "rentcast_properties_greenridge_1mi.json").open(
    encoding="utf-8"
) as file:
    greenridge = json.load(file)

original_ids = {property["id"] for property in original}
greenridge_ids = {property["id"] for property in greenridge}

print("Original records:", len(original))
print("Greenridge records:", len(greenridge))
print("Properties in both:", len(original_ids & greenridge_ids))
print("Only in original:", len(original_ids - greenridge_ids))
print("Only in Greenridge:", len(greenridge_ids - original_ids))