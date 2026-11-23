import pytest

from comp_selector import select_comps
from property import ListingStatus, Property, WaterfrontType
from valuation_readiness import ReadinessLevel, assess_valuation_readiness


def make_property(
    address: str = "Test Property",
    sqft: int | None = 2000,
    bedrooms: int | None = 3,
    bathrooms: float | None = 2.0,
    status: ListingStatus = ListingStatus.SOLD,
) -> Property:
    return Property(
        address=address,
        price=300_000,
        sqft=sqft,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        status=status,
        waterfront=WaterfrontType.INLAND,
    )


def make_candidates(primary_count: int, secondary_count: int) -> list[Property]:
    candidates = []

    for i in range(primary_count):
        candidates.append(make_property(address=f"Primary {i}"))

    for i in range(secondary_count):
        candidates.append(
            make_property(
                address=f"Secondary {i}",
                bathrooms=None,
            )
        )

    return candidates


@pytest.mark.parametrize(
    "primary_count, secondary_count, expected_level",
    [
        (3, 2, ReadinessLevel.STRONG),
        (5, 0, ReadinessLevel.STRONG),
        (2, 3, ReadinessLevel.LIMITED),
        (3, 1, ReadinessLevel.LIMITED),
        (1, 2, ReadinessLevel.LIMITED),
        (0, 5, ReadinessLevel.INSUFFICIENT),
        (1, 1, ReadinessLevel.INSUFFICIENT),
        (0, 0, ReadinessLevel.INSUFFICIENT),
    ],
)
def test_readiness_levels(primary_count, secondary_count, expected_level):
    subject = make_property(status=ListingStatus.ACTIVE)
    candidates = make_candidates(primary_count, secondary_count)

    selection = select_comps(subject, candidates)
    readiness = assess_valuation_readiness(subject, selection)

    assert readiness.level == expected_level
    assert readiness.primary_count == primary_count
    assert readiness.secondary_count == secondary_count


def test_strong_readiness_has_no_warnings():
    subject = make_property(status=ListingStatus.ACTIVE)
    selection = select_comps(subject, make_candidates(3, 2))

    readiness = assess_valuation_readiness(subject, selection)

    assert readiness.level == ReadinessLevel.STRONG
    assert readiness.warnings == []
    assert readiness.subject_completeness == pytest.approx(1.0)


def test_limited_readiness_reports_missing_primary_comps():
    subject = make_property(status=ListingStatus.ACTIVE)
    selection = select_comps(subject, make_candidates(2, 3))

    readiness = assess_valuation_readiness(subject, selection)

    assert readiness.level == ReadinessLevel.LIMITED
    assert any("At least 3 primary comps" in warning for warning in readiness.warnings)


def test_limited_readiness_reports_missing_total_comps():
    subject = make_property(status=ListingStatus.ACTIVE)
    selection = select_comps(subject, make_candidates(3, 1))

    readiness = assess_valuation_readiness(subject, selection)

    assert readiness.level == ReadinessLevel.LIMITED
    assert any("At least 5 total comps" in warning for warning in readiness.warnings)


def test_insufficient_readiness_reports_both_comp_shortages():
    subject = make_property(status=ListingStatus.ACTIVE)
    selection = select_comps(subject, make_candidates(0, 2))

    readiness = assess_valuation_readiness(subject, selection)

    assert readiness.level == ReadinessLevel.INSUFFICIENT
    assert any("At least 1 primary comp" in warning for warning in readiness.warnings)
    assert any("At least 3 total comps" in warning for warning in readiness.warnings)


def test_missing_square_footage_prevents_readiness():
    subject = make_property(
        sqft=None,
        status=ListingStatus.ACTIVE,
    )
    selection = select_comps(subject, make_candidates(3, 2))

    readiness = assess_valuation_readiness(subject, selection)

    assert readiness.level == ReadinessLevel.INSUFFICIENT
    assert any("square footage is missing" in warning for warning in readiness.warnings)


def test_missing_bathrooms_generates_warning():
    subject = make_property(
        bathrooms=None,
        status=ListingStatus.ACTIVE,
    )
    selection = select_comps(subject, make_candidates(3, 2))

    readiness = assess_valuation_readiness(subject, selection)

    assert readiness.level == ReadinessLevel.INSUFFICIENT
    assert readiness.primary_count == 0
    assert readiness.secondary_count == 5
    assert any("bathroom count is missing" in warning for warning in readiness.warnings)
    assert any("At least 80 percent" in warning for warning in readiness.warnings)


def test_missing_bedrooms_generates_warning():
    subject = make_property(
        bedrooms=None,
        status=ListingStatus.ACTIVE,
    )
    selection = select_comps(subject, make_candidates(3, 2))

    readiness = assess_valuation_readiness(subject, selection)

    assert readiness.level == ReadinessLevel.INSUFFICIENT
    assert readiness.primary_count == 0
    assert readiness.secondary_count == 3
    assert any("bedroom count is missing" in warning for warning in readiness.warnings)


def test_multiple_warnings_can_be_returned():
    subject = make_property(
        sqft=None,
        bedrooms=None,
        bathrooms=None,
        status=ListingStatus.ACTIVE,
    )
    selection = select_comps(subject, make_candidates(0, 0))

    readiness = assess_valuation_readiness(subject, selection)

    assert readiness.level == ReadinessLevel.INSUFFICIENT
    assert len(readiness.warnings) >= 6
    assert readiness.subject_completeness == pytest.approx(0.0)


def test_readiness_uses_all_qualifying_comps_not_preview_limit():
    subject = make_property(status=ListingStatus.ACTIVE)
    selection = select_comps(
        subject,
        make_candidates(6, 3),
        limit=2,
    )

    readiness = assess_valuation_readiness(subject, selection)

    assert len(selection.primary) == 2
    assert len(selection.secondary) == 2
    assert readiness.primary_count == 6
    assert readiness.secondary_count == 3
    assert readiness.level == ReadinessLevel.STRONG
