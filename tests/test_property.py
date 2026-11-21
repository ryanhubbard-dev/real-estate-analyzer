import pytest
from property import Property, ListingStatus, WaterfrontType


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
        sqft=None,
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


def test_property_classification_defaults():
    house = Property(
        address="Example House",
        price=300000,
        bedrooms=4,
        sqft=1800,
        bathrooms=2.5
    )

    assert house.status == ListingStatus.ACTIVE
    assert house.waterfront == WaterfrontType.UNKNOWN


def test_property_classification():
    house = Property(
        address="Waterfront House",
        price=450000,
        bedrooms=4,
        sqft=2000,
        bathrooms=3,
        status=ListingStatus.SOLD,
        waterfront=WaterfrontType.WATERFRONT
    )

    assert house.status == ListingStatus.SOLD
    assert house.waterfront == WaterfrontType.WATERFRONT


@pytest.mark.parametrize(
    "status",
    ["active", "banana", None]
)
def test_invalid_status(status):
    with pytest.raises(ValueError):
        Property(
            address="Waterfront House",
            price=450000,
            bedrooms=4,
            sqft=2000,
            bathrooms=3,
            status=status
        )


@pytest.mark.parametrize(
    "waterfront",
    ["waterfront", "oceanfront", None]
)
def test_invalid_waterfront(waterfront):
    with pytest.raises(
        ValueError,
        match="Waterfront must be a WaterfrontType enum."
    ):
        Property(
            address="Example House",
            price=300000,
            bedrooms=4,
            sqft=1800,
            bathrooms=2.5,
            waterfront=waterfront
        )

