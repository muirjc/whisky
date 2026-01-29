"""FlavorProfile Pydantic schema for whisky tasting profiles."""

from pydantic import BaseModel, Field


class FlavorProfile(BaseModel):
    """Flavor intensity ratings for a whisky (0-5 scale)."""

    smoky_peaty: int = Field(0, ge=0, le=5, description="Smoky/Peaty intensity")
    fruity: int = Field(0, ge=0, le=5, description="Fruity (citrus, orchard, tropical)")
    sherried: int = Field(0, ge=0, le=5, description="Sherried (dried fruit, rich)")
    spicy: int = Field(0, ge=0, le=5, description="Spicy (pepper, cinnamon)")
    floral_grassy: int = Field(0, ge=0, le=5, description="Floral/Grassy notes")
    maritime: int = Field(0, ge=0, le=5, description="Maritime (brine, seaweed)")
    honey_sweet: int = Field(0, ge=0, le=5, description="Honey/Sweet notes")
    vanilla_caramel: int = Field(0, ge=0, le=5, description="Vanilla/Caramel notes")
    oak_woody: int = Field(0, ge=0, le=5, description="Oak/Woody character")
    nutty: int = Field(0, ge=0, le=5, description="Nutty notes")
    malty_biscuity: int = Field(0, ge=0, le=5, description="Malty/Biscuity character")
    medicinal_iodine: int = Field(0, ge=0, le=5, description="Medicinal/Iodine notes")

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "smoky_peaty": 4,
                "fruity": 2,
                "sherried": 3,
                "spicy": 2,
                "floral_grassy": 1,
                "maritime": 4,
                "honey_sweet": 2,
                "vanilla_caramel": 2,
                "oak_woody": 3,
                "nutty": 1,
                "malty_biscuity": 2,
                "medicinal_iodine": 3,
            }
        }

    def to_dict(self) -> dict[str, int]:
        """Convert to dictionary for storage."""
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict[str, int] | None) -> "FlavorProfile":
        """Create from dictionary, with defaults for missing values."""
        if not data:
            return cls(**{f: 0 for f in cls.model_fields})
        return cls(**{k: v for k, v in data.items() if k in cls.model_fields})

    def to_vector(self) -> list[int]:
        """Convert to vector for similarity calculations."""
        return [
            self.smoky_peaty,
            self.fruity,
            self.sherried,
            self.spicy,
            self.floral_grassy,
            self.maritime,
            self.honey_sweet,
            self.vanilla_caramel,
            self.oak_woody,
            self.nutty,
            self.malty_biscuity,
            self.medicinal_iodine,
        ]

    @classmethod
    def field_names(cls) -> list[str]:
        """Get ordered list of flavor field names."""
        return [
            "smoky_peaty",
            "fruity",
            "sherried",
            "spicy",
            "floral_grassy",
            "maritime",
            "honey_sweet",
            "vanilla_caramel",
            "oak_woody",
            "nutty",
            "malty_biscuity",
            "medicinal_iodine",
        ]
