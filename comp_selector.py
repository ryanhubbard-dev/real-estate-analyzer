from dataclasses import dataclass

from comparable import (
    are_comparable,
    comparison_coverage,
    data_completeness,
    overall_similarity,
)
from property import ListingStatus, Property


@dataclass
class ScoredComp:
    property: Property
    similarity: float
    completeness: float
    coverage: float


@dataclass
class CompSelection:
    primary: list[ScoredComp]
    secondary: list[ScoredComp]
    primary_count: int
    secondary_count: int
    all_primary: list[ScoredComp]
    all_secondary: list[ScoredComp]


def select_comps(subject: Property, candidates: list[Property], limit: int = 5,) -> CompSelection:
    primary: list[ScoredComp] = []
    secondary: list[ScoredComp] = []

    for candidate in candidates:
        if candidate.status != ListingStatus.SOLD:
            continue

        if candidate is subject:
            continue

        if not are_comparable(subject, candidate):
            continue

        similarity = overall_similarity(subject, candidate)
        if similarity is None:
            continue

        completeness = data_completeness(candidate)
        coverage = comparison_coverage(subject, candidate)

        scored_comp = ScoredComp(candidate, similarity, completeness, coverage)

        if coverage >= 0.80:
            primary.append(scored_comp)
        elif coverage >= 0.50:
            secondary.append(scored_comp)

    primary.sort(key=lambda comp: comp.similarity, reverse=True)
    secondary.sort(key=lambda comp: comp.similarity, reverse=True)

    return CompSelection(
        primary=primary[:limit],
        secondary=secondary[:limit],
        primary_count=len(primary),
        secondary_count=len(secondary),
        all_primary=primary,
        all_secondary=secondary,
    )