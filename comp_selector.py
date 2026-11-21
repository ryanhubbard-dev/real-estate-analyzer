from dataclasses import dataclass

from comparable import are_comparable, overall_similarity
from property import ListingStatus, Property


@dataclass
class ScoredComp:
    property: Property
    similarity: float


def select_comps(subject: Property, candidates: list[Property], limit: int = 5) -> list[ScoredComp]:
    scored_comps: list[ScoredComp] = []

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

        scored_comps.append(ScoredComp(candidate, similarity))

    scored_comps.sort(key=lambda comp: comp.similarity, reverse=True)
    return scored_comps[:limit]