from property import Property


house1 = Property(
    address="Example House A",
    price=325000,
    bedrooms=4,
    sqft=1800,
    bathrooms=2.5
)

house2 = Property(
    address="Example House B",
    price=275000,
    bedrooms=3
)

print("PROPERTY 1")
print(house1)
print(f"Price per sqft: ${house1.price_per_sqft:.2f}")

print("\nPROPERTY 2")
print(house2)
print(f"Price per sqft: {house2.price_per_sqft}")

house1.price = 300000

print("\nAFTER PRICE REDUCTION")
print(f"Updated price per sqft: ${house1.price_per_sqft:.2f}\n")
try:
    house3 = Property(
        address="Invalid Property",
        price=250000,
        bedrooms=3,
        sqft=0
    )
except ValueError as error:
    print(f"Invalid property data: {error}")
