from enum import Enum

PinCategories = Enum(
    "PinCategories",
    [
        ("DUMP", "Dumping"),
        ("ACTIVE", "Encampment Trash"),
        ("INACTIVE", "Inactive Encampment"),
        ("LIT", "Litter"),
        ("SPEC", "Special Removal Needed"),
        ("STORM", "Stormwater Debris"),
    ],
)
