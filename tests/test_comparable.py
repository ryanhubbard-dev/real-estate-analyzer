import pytest

from comparable import are_comparable
from property import Property, WaterfrontType


@pytest.mark.parametrize(
    "subject_type, candidate_type, expected",
    [
        (WaterfrontType.WATERFRONT, WaterfrontType.WATERFRONT, True),
        (WaterfrontType.WATERFRONT, WaterfrontType.INLAND, False),
        (WaterfrontType.INLAND, WaterfrontType.WATERFRONT, False),
        (WaterfrontType.LAKE_VIEW, WaterfrontType.INLAND, True),
        (WaterfrontType.INLAND, WaterfrontType.LAKE_VIEW, True),
        (WaterfrontType.INLAND, WaterfrontType.INLAND, True),
        (WaterfrontType.UNKNOWN, WaterfrontType.INLAND, False),
        (WaterfrontType.UNKNOWN, WaterfrontType.UNKNOWN, False),
    ]
)
def test_are_comparable(subject_type, candidate_type, expected):
    subject = Property(
        address="Subject House",
        price=450000,
        bedrooms=4,
        sqft=2000,
        bathrooms=3,
        waterfront=subject_type
    )

    candidate = Property(
        address="Candidate House",
        price=450000,
        bedrooms=4,
        sqft=2000,
        bathrooms=3,
        waterfront=candidate_type
    )

    assert are_comparable(subject, candidate) is expected