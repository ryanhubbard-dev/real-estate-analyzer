from property import Property, WaterfrontType


def are_comparable(subject: Property, candidate: Property) -> bool:
    if WaterfrontType.UNKNOWN in (subject.waterfront, candidate.waterfront):
        return False
    
    if WaterfrontType.WATERFRONT in (subject.waterfront, candidate.waterfront):
        return subject.waterfront == candidate.waterfront

    return True
