import pytest

from comp_selector import select_comps
from property import ListingStatus, Property, WaterfrontType


@pytest.mark.parametrize(
    "status, waterfront, expected_count",
    [
        (ListingStatus.ACTIVE, WaterfrontType.INLAND, 0),
        (ListingStatus.PENDING, WaterfrontType.INLAND, 0),
        (ListingStatus.SOLD, WaterfrontType.INLAND, 1),
        (ListingStatus.SOLD, WaterfrontType.LAKE_VIEW, 1),
        (ListingStatus.SOLD, WaterfrontType.WATERFRONT, 0),
        (ListingStatus.SOLD, WaterfrontType.UNKNOWN, 0),
    ],
)
def test_select_comps_filtering(status, waterfront, expected_count):
    subject = Property(
        address="Subject House",
        price=450000,
        bedrooms=4,
        sqft=2000,
        bathrooms=2.5,
        waterfront=WaterfrontType.INLAND,
    )

    candidate = Property(
        address="Candidate House",
        price=350000,
        bedrooms=3,
        sqft=1800,
        bathrooms=2.0,
        status=status,
        waterfront=waterfront,
    )

    results = select_comps(subject, [candidate])

    assert results.primary_count == expected_count
    assert results.secondary_count == 0


def test_select_comps_empty():
    subject = Property(
        address="Subject House",
        price=450000,
        sqft=2000,
        bedrooms=4,
        waterfront=WaterfrontType.INLAND,
    )

    results = select_comps(subject, [])

    assert results.primary == []
    assert results.secondary == []
    assert results.primary_count == 0
    assert results.secondary_count == 0


def test_select_comps_excludes_subject():
    subject = Property(
        address="Subject House",
        price=450000,
        sqft=2000,
        bedrooms=4,
        status=ListingStatus.SOLD,
        waterfront=WaterfrontType.INLAND,
    )

    results = select_comps(subject, [subject])

    assert results.primary_count == 0
    assert results.secondary_count == 0


def test_select_comps_ranking():
    subject = Property(
        address="Subject",
        price=400000,
        bedrooms=3,
        sqft=2000,
        bathrooms=2.0,
        waterfront=WaterfrontType.INLAND,
    )

    candidates = [
        Property("Poor Match", 300000, 1000, 3, 2.0, ListingStatus.SOLD, WaterfrontType.INLAND),
        Property("Best Match", 300000, 2000, 3, 2.0, ListingStatus.SOLD, WaterfrontType.INLAND),
        Property("Good Match", 300000, 1800, 3, 2.0, ListingStatus.SOLD, WaterfrontType.INLAND),
        Property("Fair Match", 300000, 1500, 3, 2.0, ListingStatus.SOLD, WaterfrontType.INLAND),
    ]

    results = select_comps(subject, candidates)

    assert [comp.property.address for comp in results.primary] == [
        "Best Match", "Good Match", "Fair Match", "Poor Match"
    ]

    assert results.primary[0].similarity == pytest.approx(1.0)
    assert results.primary[1].similarity == pytest.approx(0.953846)
    assert results.primary[2].similarity == pytest.approx(0.884615)
    assert results.primary[3].similarity == pytest.approx(0.769231)


def test_select_comps_ties():
    subject = Property("Subject", 400000, 2000, 3, 2.0, waterfront=WaterfrontType.INLAND)
    candidate1 = Property("Comp A", 350000, 2000, 3, 2.0, ListingStatus.SOLD, WaterfrontType.INLAND)
    candidate2 = Property("Comp B", 375000, 2000, 3, 2.0, ListingStatus.SOLD, WaterfrontType.INLAND)

    results = select_comps(subject, [candidate1, candidate2])

    assert results.primary_count == 2
    assert [comp.property.address for comp in results.primary] == ["Comp A", "Comp B"]
    assert all(comp.similarity == pytest.approx(1.0) for comp in results.primary)


def test_select_comps_missing_data():
    subject = Property("Subject", 400000, None, 3, None, waterfront=WaterfrontType.INLAND)
    candidate = Property("Comp A", 350000, None, 2, None, ListingStatus.SOLD, WaterfrontType.INLAND)

    results = select_comps(subject, [candidate])

    # Only bedrooms overlap, giving 30.77% coverage.
    assert results.primary_count == 0
    assert results.secondary_count == 0


@pytest.mark.parametrize("limit, expected_count", [(5, 5), (3, 3), (1, 1)])
def test_select_comps_limit(limit, expected_count):
    subject = Property("Subject", 400000, 2000, 3, 2.0, waterfront=WaterfrontType.INLAND)

    candidates = [
        Property(f"Comp {sqft}", 350000, sqft, 3, 2.0, ListingStatus.SOLD, WaterfrontType.INLAND)
        for sqft in [1000, 1200, 1400, 1600, 1800, 2000]
    ]

    results = select_comps(subject, candidates, limit=limit)

    assert len(results.primary) == expected_count
    assert results.primary_count == 6
    assert len(results.all_primary) == 6
    assert results.primary[0].property.sqft == 2000
    assert [comp.property.sqft for comp in results.primary] == [
        2000, 1800, 1600, 1400, 1200
    ][:limit]


def test_select_comps_separates_primary_and_secondary():
    subject = Property(
        "Subject", 400000, 2000, 3, 2.0,
        waterfront=WaterfrontType.INLAND,
    )

    primary = Property(
        "Primary", 350000, 1900, 3, 2.0,
        status=ListingStatus.SOLD,
        waterfront=WaterfrontType.INLAND,
    )

    secondary = Property(
        "Secondary", 330000, 1900, 3, None,
        status=ListingStatus.SOLD,
        waterfront=WaterfrontType.INLAND,
    )

    results = select_comps(subject, [primary, secondary])

    assert results.primary_count == 1
    assert results.secondary_count == 1
    assert results.primary[0].property is primary
    assert results.secondary[0].property is secondary


def test_select_comps_preserves_all_qualifying_results():
    subject = Property(
        "Subject", 400000, 2000, 3, 2.0,
        waterfront=WaterfrontType.INLAND,
    )

    candidates = [
        Property(
            f"Comp {i}", 350000, 2000 + i * 50, 3, 2.0,
            status=ListingStatus.SOLD,
            waterfront=WaterfrontType.INLAND,
        )
        for i in range(8)
    ]

    results = select_comps(subject, candidates)

    assert results.primary_count == 8
    assert len(results.primary) == 5
    assert len(results.all_primary) == 8
    assert results.secondary_count == 0

    similarities = [comp.similarity for comp in results.all_primary]
    assert similarities == sorted(similarities, reverse=True)