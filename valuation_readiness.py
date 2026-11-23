from dataclasses import dataclass
from enum import Enum

from comp_selector import CompSelection
from comparable import data_completeness
from property import Property


class ReadinessLevel(Enum):
    STRONG = "strong"
    LIMITED = "limited"
    INSUFFICIENT = "insufficient"


@dataclass
class ValuationReadiness:
    level: ReadinessLevel
    primary_count: int
    secondary_count: int
    subject_completeness: float
    warnings: list[str]


def assess_valuation_readiness(subject: Property, selection: CompSelection) -> ValuationReadiness:
    total_comps = selection.primary_count + selection.secondary_count
    completeness = data_completeness(subject)
    has_sqft = subject.sqft is not None

    if has_sqft and completeness >= 0.80 and selection.primary_count >= 3 and total_comps >= 5:
        level = ReadinessLevel.STRONG
    elif has_sqft and completeness >= 0.50 and selection.primary_count >= 1 and total_comps >= 3:
        level = ReadinessLevel.LIMITED
    else:
        level = ReadinessLevel.INSUFFICIENT

    warnings = []

    if not has_sqft:
        warnings.append(
            "Subject square footage is missing. "
            "Verify square footage before estimating market value."
        )

    if subject.bedrooms is None:
        warnings.append(
            "Subject bedroom count is missing. Verify the number of bedrooms."
        )

    if subject.bathrooms is None:
        warnings.append(
            "Subject bathroom count is missing. Verify the number of bathrooms."
        )

    if completeness < 0.50:
        warnings.append(
            f"Subject data completeness is {completeness:.1%}. "
            "At least 50 percent is required for limited valuation readiness."
        )
    elif completeness < 0.80:
        warnings.append(
            f"Subject data completeness is {completeness:.1%}. "
            "At least 80 percent is required for strong valuation readiness."
        )

    if selection.primary_count < 1:
        warnings.append(
            f"Only {selection.primary_count} primary comps available. "
            "At least 1 primary comp is required for limited readiness. "
            "Find additional qualifying sold properties."
        )
    elif selection.primary_count < 3:
        warnings.append(
            f"Only {selection.primary_count} primary comps available. "
            "At least 3 primary comps are required for strong readiness. "
            "Find additional qualifying sold properties."
        )

    if total_comps < 3:
        warnings.append(
            f"Only {total_comps} qualifying comps available. "
            "At least 3 total comps are required for limited readiness. "
            "Find additional qualifying sold properties."
        )
    elif total_comps < 5:
        warnings.append(
            f"Only {total_comps} qualifying comps available. "
            "At least 5 total comps are required for strong readiness. "
            "Find additional qualifying sold properties."
        )

    return ValuationReadiness(
        level=level,
        primary_count=selection.primary_count,
        secondary_count=selection.secondary_count,
        subject_completeness=completeness,
        warnings=warnings,
    )
