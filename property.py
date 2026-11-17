from dataclasses import dataclass


@dataclass
class Property:
    address: str
    price: int
    bedrooms: int
    sqft: int | None = None    
    bathrooms: float | None = None

    def __post_init__(self):
        if self.price <= 0:
            raise ValueError("Price must be greater than zero.")

        if self.sqft is not None and self.sqft <= 0:
            raise ValueError("Square footage must be greater than zero.")

        if self.bedrooms < 0:
            raise ValueError("Bedrooms cannot be negative.")

        if self.bathrooms is not None and self.bathrooms < 0:
            raise ValueError("Bathrooms cannot be negative.")

    @property
    def price_per_sqft(self) -> float | None:
        if self.sqft is None:
            return None

        return self.price / self.sqft
