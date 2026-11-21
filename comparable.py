from property import Property, WaterfrontType
SQFT_WEIGHT = 0.30
BEDROOM_WEIGHT = 0.20
BATHROOM_WEIGHT = 0.15

TOTAL_WEIGHT = SQFT_WEIGHT + BEDROOM_WEIGHT + BATHROOM_WEIGHT


def overall_similarity(subject: Property, candidate: Property) -> float | None:
    weighted_sum = 0.0
    total_weight = 0.0 
    
    sqft_score = sqft_similarity(subject, candidate)
    bedroom_score = bedroom_similarity(subject, candidate)
    bathroom_score = bathroom_similarity(subject, candidate)

    if sqft_score is not None:
        weighted_sum += sqft_score * SQFT_WEIGHT
        total_weight += SQFT_WEIGHT

    if bedroom_score is not None:
        weighted_sum += bedroom_score * BEDROOM_WEIGHT
        total_weight += BEDROOM_WEIGHT

    if bathroom_score is not None:
        weighted_sum += bathroom_score * BATHROOM_WEIGHT
        total_weight += BATHROOM_WEIGHT

    if total_weight == 0:
        return None

    return weighted_sum / total_weight


def data_completeness(property: Property) -> float:
    available_weight = 0.0

    if property.sqft is not None:
        available_weight += SQFT_WEIGHT

    if property.bedrooms is not None:
        available_weight += BEDROOM_WEIGHT

    if property.bathrooms is not None:
        available_weight += BATHROOM_WEIGHT

    return available_weight / TOTAL_WEIGHT


def comparison_coverage(subject: Property, candidate: Property) -> float:
    available_weight = 0.0

    if subject.sqft is not None and candidate.sqft is not None:
        available_weight += SQFT_WEIGHT

    if subject.bedrooms is not None and candidate.bedrooms is not None:
        available_weight += BEDROOM_WEIGHT

    if subject.bathrooms is not None and candidate.bathrooms is not None:
        available_weight += BATHROOM_WEIGHT

    return available_weight / TOTAL_WEIGHT


def are_comparable(subject: Property, candidate: Property) -> bool:
    if WaterfrontType.UNKNOWN in (subject.waterfront, candidate.waterfront):
        return False
    
    if WaterfrontType.WATERFRONT in (subject.waterfront, candidate.waterfront):
        return subject.waterfront == candidate.waterfront

    return True


def sqft_similarity(subject: Property, candidate: Property) -> float | None:
    if subject.sqft is None or candidate.sqft is None:
        return None

    smaller = min(subject.sqft, candidate.sqft)
    larger = max(subject.sqft, candidate.sqft)

    return smaller / larger


def bedroom_similarity(subject: Property, candidate: Property) -> float | None:
    if subject.bedrooms is None or candidate.bedrooms is None:
        return None
    
    smaller = min(subject.bedrooms, candidate.bedrooms)
    larger = max(subject.bedrooms, candidate.bedrooms)

    return ((smaller + 1) / (larger + 1)) ** 0.7


def bathroom_similarity(subject: Property, candidate: Property) -> float | None:
    if subject.bathrooms is None or candidate.bathrooms is None:
        return None

    smaller = min(subject.bathrooms, candidate.bathrooms)
    larger = max(subject.bathrooms, candidate.bathrooms)

    return ((smaller + 0.5) / (larger + 0.5)) ** 0.7