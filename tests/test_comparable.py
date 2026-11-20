import pytest

from comparable import (
    are_comparable,
    sqft_similarity,
    bedroom_similarity,
    bathroom_similarity,
    overall_similarity,
)    
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


@pytest.mark.parametrize(
    "subject_sqft, candidate_sqft, expected",
    [
        (2000, 2000, 1.0),
        (2000, 1800, 0.9),
        (1800, 2000, 0.9),
        (2000, 1000, 0.5),
        (1800, 1500, 5 / 6),
    ]
)
def test_sqft_similarity(subject_sqft, candidate_sqft, expected):
    subject = Property(
        address="Subject House",
        price=450000,
        bedrooms=4,
        sqft=subject_sqft,
    )

    candidate = Property(
        address="Candidate House",
        price=450000,
        bedrooms=4,
        sqft=candidate_sqft,
    )

    assert sqft_similarity(subject, candidate) == pytest.approx(expected)


@pytest.mark.parametrize(
    "subject_sqft, candidate_sqft",
    [
        (None, 2000),
        (2000, None),
        (None, None),
    ]
)
def test_sqft_similarity_missing(subject_sqft, candidate_sqft):
    subject = Property(
        address="Subject House",
        price=450000,
        bedrooms=4,
        sqft=subject_sqft,
    )

    candidate = Property(
        address="Candidate House",
        price=450000,
        bedrooms=4,
        sqft=candidate_sqft,
    )

    assert sqft_similarity(subject, candidate) is None


@pytest.mark.parametrize(
    "subject_bedrooms, candidate_bedrooms, expected",
    [
        (0, 0, 1.0),
        (0, 1, 0.6155722),
        (1, 2, 0.7528979),
        (2, 3, 0.8176037),
        (3, 2, 0.8176037),
        (2, 1, 0.7528979),
        (1, 0, 0.6155722),
        (6, 7, 0.9107635),
        (1, 3, 0.6155722),
    ]
)
def test_bedroom_similarity(subject_bedrooms, candidate_bedrooms, expected):
    subject = Property(
        address="Subject House",
        price=450000,
        bedrooms=subject_bedrooms,
        sqft=2000,
    )

    candidate = Property(
        address="Candidate House",
        price=450000,
        bedrooms=candidate_bedrooms,
        sqft=2000,
    )

    assert bedroom_similarity(subject, candidate) == pytest.approx(expected)


@pytest.mark.parametrize(
    "subject_bathrooms, candidate_bathrooms, expected",
    [
        (0, 0, 1.0000),
        (0, 1, 0.4635),
        (1, 1, 1.0000),
        (1, 1.5, 0.8176),
        (1, 2, 0.6993),
        (2, 2.5, 0.8805),
        (2, 3, 0.7901),
        (3, 2, 0.7901),
    ]
)
def test_bathroom_similarity(subject_bathrooms, candidate_bathrooms, expected):
    subject = Property(
        address="Subject House",
        price=450000,
        bedrooms=4,
        sqft=2000,
        bathrooms=subject_bathrooms,
    )

    candidate = Property(
        address="Candidate House",
        price=450000,
        bedrooms=4,
        sqft=2000,
        bathrooms=candidate_bathrooms,
    )

    assert bathroom_similarity(subject, candidate) == pytest.approx(expected, abs=0.0005)


@pytest.mark.parametrize(
    "subject_bathrooms, candidate_bathrooms",
    [
        (None, 2.0),
        (2.0, None),
        (None, None),
    ]
)
def test_bathroom_similarity_missing(subject_bathrooms, candidate_bathrooms):
    subject = Property(
        address="Subject House",
        price=450000,
        bedrooms=4,
        sqft=2000,
        bathrooms=subject_bathrooms,
    )

    candidate = Property(
        address="Candidate House",
        price=450000,
        bedrooms=4,
        sqft=2000,
        bathrooms=candidate_bathrooms,
    )

    assert bathroom_similarity(subject, candidate) is None


@pytest.mark.parametrize(
    "subject_sqft, candidate_sqft, subject_bed, candidate_bed, subject_bath, candidate_bath, expected",
    [
        # Identical properties
        (2000, 2000, 3, 3, 2.0, 2.0, 1.0),

        # Square footage differences
        (2000, 1800, 3, 3, 2.0, 2.0, 0.953846),
        (1800, 2000, 3, 3, 2.0, 2.0, 0.953846),
        (2000, 1000, 3, 3, 2.0, 2.0, 0.769231),

        # Bedroom differences
        (2000, 2000, 2, 3, 2.0, 2.0, 0.943878),
        (2000, 2000, 3, 2, 2.0, 2.0, 0.943878),

        # Bathroom differences
        (2000, 2000, 3, 3, 1.0, 2.0, 0.930623),

        # Missing square footage
        (None, 2000, 3, 3, 2.0, 2.0, 1.0),

        # Missing bathrooms
        (2000, 2000, 3, 3, None, 2.0, 1.0),

        # Only bedrooms available
        (None, None, 2, 3, None, None, 0.817604),

        # Zero-bedroom properties
        (2000, 2000, 0, 0, 2.0, 2.0, 1.0),
        (2000, 2000, 0, 1, 2.0, 2.0, 0.881714),
    ],
)
def test_overall_similarity(
    subject_sqft,
    candidate_sqft,
    subject_bed,
    candidate_bed,
    subject_bath,
    candidate_bath,
    expected,
):
    subject = Property(
        address="Subject House",
        price=450000,
        bedrooms=subject_bed,
        sqft=subject_sqft,
        bathrooms=subject_bath,
    )
    candidate = Property(
        address="Candidate House",
        price=450000,
        bedrooms=candidate_bed,
        sqft=candidate_sqft,
        bathrooms=candidate_bath,
    )

    assert overall_similarity(subject, candidate) == pytest.approx(expected, abs=0.000001)