import json
from collections import Counter
from pathlib import Path

file_path = Path("data/rentcast_properties_merged.json")

with file_path.open("r", encoding="utf-8") as file:
    properties = json.load(file)

print(f"Total records loaded: {len(properties)}")

print("\nFields available in the first property:")
for field, value in properties[0].items():
    print(f"{field}: {type(value).__name__}")

fields = [
    "squareFootage",
    "bedrooms",
    "bathrooms",
    "lotSize",
    "yearBuilt",
    "latitude",
    "longitude",
    "subdivision",
    "lastSaleDate",
    "lastSalePrice",
]

print("\nDATA COMPLETENESS REPORT")
print("-" * 50)

for field in fields:
    populated = sum(
        property.get(field) is not None
        for property in properties
    )

    percentage = populated / len(properties) * 100

    print(f"{field:<20} {populated:>3}/{len(properties)} ({percentage:5.1f}%)")


subdivisions = Counter(
    property.get("subdivision") or "UNKNOWN"
    for property in properties
)

print("\nSUBDIVISION BREAKDOWN")
print("-" * 50)

for subdivision, count in subdivisions.most_common(20):
    print(f"{subdivision:<35} {count:>4}")

cape_royale = []
unknown = []
other = []

for property_data in properties:
    subdivision = property_data.get("subdivision")

    if not subdivision:
        unknown.append(property_data)
    elif "CAPE ROYALE" in subdivision.upper():
        cape_royale.append(property_data)
    else:
        other.append(property_data)

print("\nCAPE ROYALE MEMBERSHIP AUDIT")
print("-" * 50)
print(f"Cape Royale labeled: {len(cape_royale)}")
print(f"Unknown subdivision: {len(unknown)}")
print(f"Other subdivisions: {len(other)}")

print("\nOTHER SUBDIVISIONS")
for subdivision, count in Counter(
    property_data["subdivision"] for property_data in other
).most_common():
    print(f"{subdivision}: {count}")