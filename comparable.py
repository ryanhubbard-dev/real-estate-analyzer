from property import Property, WaterfrontType


def overall_similarity(subject: Property, candidate: Property) -> float | None:
    weighted_sum = 0.0
    total_weight = 0.0 
    
    sqft_score = sqft_similarity(subject, candidate)
    bedroom_score = bedroom_similarity(subject, candidate)
    bathroom_score = bathroom_similarity(subject, candidate)

    if sqft_score is not None:
        weighted_sum += sqft_score * 0.30
        total_weight += 0.30

    if bedroom_score is not None:
        weighted_sum += bedroom_score * 0.20
        total_weight += 0.20

    if bathroom_score is not None:
        weighted_sum += bathroom_score * 0.15
        total_weight += 0.15

    if total_weight == 0:
        return None

    return weighted_sum / total_weight

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


def bedroom_similarity(subject: Property, candidate: Property) -> float:
    smaller = min(subject.bedrooms, candidate.bedrooms)
    larger = max(subject.bedrooms, candidate.bedrooms)

    return ((smaller + 1) / (larger + 1)) ** 0.7


def bathroom_similarity(subject: Property, candidate: Property) -> float | None:
    if subject.bathrooms is None or candidate.bathrooms is None:
        return None

    smaller = min(subject.bathrooms, candidate.bathrooms)
    larger = max(subject.bathrooms, candidate.bathrooms)

    return ((smaller + 0.5) / (larger + 0.5)) ** 0.7