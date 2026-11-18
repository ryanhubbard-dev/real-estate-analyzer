import pytest
from property import Property


def test_property_creation():
    house = Property(
        address="Example House",
        price=300000,
        bedrooms=4,
        sqft=1800,
        bathrooms=2.5
    )

    assert house.price == 300000
    assert house.sqft == 1800


def test_missing_sqft():
    house = Property(
        address="Example House",
        price=300000,
        bedrooms=4,
        bathrooms=2.5
    )

    assert house.sqft is None
    assert house.price_per_sqft is None

@pytest.mark.parametrize(
    "sqft",
    [0, -1, -500]
)
def test_invalid_sqft(sqft):
    with pytest.raises(ValueError):
        Property(
            address="Example House",
            price=300000,
            bedrooms=4,
            sqft=sqft,
            bathrooms=2.5
        )

@pytest.mark.parametrize(
    "price, sqft, expected",
    [
        (360000, 2000, 180),
        (250000, 1000, 250),
        (325000, 1800, 180.5555555556),
    ]
)
def test_price_per_sqft(price, sqft, expected):
    house = Property(
        address="Example House",
        price=price,
        bedrooms=4,
        sqft=sqft
    )

    assert house.price_per_sqft == pytest.approx(expected)