from dataclasses import dataclass
from enum import Enum


class ListingStatus(Enum):
    ACTIVE = "active"
    PENDING = "pending"
    SOLD = "sold"


class WaterfrontType(Enum):
    WATERFRONT = "waterfront"
    LAKE_VIEW = "lake_view"
    INLAND = "inland"
    UNKNOWN = "unknown"

@dataclass
class Property:
    address: str
    price: int
    sqft: int | None
    bedrooms: int | None
    bathrooms: float | None = None
    status: ListingStatus = ListingStatus.ACTIVE
    waterfront: WaterfrontType = WaterfrontType.UNKNOWN

    def __post_init__(self):
        if self.price <= 0:
            raise ValueError("Price must be greater than zero.")

        if self.sqft is not None and self.sqft <= 0:
            raise ValueError("Square footage must be greater than zero.")

        if self.bedrooms is not None and self.bedrooms < 0:
            raise ValueError("Bedrooms cannot be negative.")

        if self.bathrooms is not None and self.bathrooms < 0:
            raise ValueError("Bathrooms cannot be negative.")

        if not isinstance(self.status, ListingStatus):
            raise ValueError("Status must be a ListingStatus enum.")

        if not isinstance(self.waterfront, WaterfrontType):
            raise ValueError("Waterfront must be a WaterfrontType enum.")

    @property
    def price_per_sqft(self) -> float | None:
        if self.sqft is None:
            return None

        return self.price / self.sqft
