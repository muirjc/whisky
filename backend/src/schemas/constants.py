"""Constants for regions, countries, and other reference data."""

# Whisky regions organized by country
WHISKY_REGIONS: dict[str, list[str]] = {
    "Scotland": [
        "Speyside",
        "Highland",
        "Lowland",
        "Islay",
        "Campbeltown",
        "Islands",
    ],
    "Ireland": [
        "Single Pot Still",
        "Single Malt",
        "Blended",
    ],
    "USA": [
        "Kentucky",
        "Tennessee",
        "Other US",
    ],
    "Japan": [
        "Japanese",
    ],
    "Canada": [
        "Canadian",
    ],
    "India": [
        "Indian",
    ],
    "Taiwan": [
        "Taiwanese",
    ],
    "Australia": [
        "Australian",
    ],
    "Other": [
        "Other",
    ],
}

# Flat list of all countries
WHISKY_COUNTRIES: list[str] = list(WHISKY_REGIONS.keys())

# Flat list of all regions
ALL_REGIONS: list[str] = [
    region for regions in WHISKY_REGIONS.values() for region in regions
]

# Standard bottle sizes in milliliters
BOTTLE_SIZES_ML: list[int] = [
    50,    # Miniature
    200,   # Flask
    350,   # Small
    500,   # Half bottle
    700,   # Standard (EU)
    750,   # Standard (US)
    1000,  # Liter
    1750,  # Magnum
]


def get_regions_for_country(country: str) -> list[str]:
    """Get valid regions for a given country."""
    return WHISKY_REGIONS.get(country, ["Other"])


def is_valid_region(region: str, country: str | None = None) -> bool:
    """Check if a region is valid, optionally for a specific country."""
    if country:
        return region in get_regions_for_country(country)
    return region in ALL_REGIONS


def is_valid_country(country: str) -> bool:
    """Check if a country is in the valid list."""
    return country in WHISKY_COUNTRIES
