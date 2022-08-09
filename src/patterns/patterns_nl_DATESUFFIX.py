patterns_nl_DATESUFFIX = [
    { 
        "label": "DATESUFFIX", 
        "language": "nl",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": r"cal\.?"}},
            {"LOWER": {"REGEX": r"^(ad|bce?|bp|a\.d\.|b\.c\.|b\.c\.e\.|b\.p\.)$"}}
        ]
    },
    { 
        "label": "DATESUFFIX", 
        "language": "nl",
        "pattern": [
            {"LOWER": {"REGEX": r"^(na?\.?|voor|vóór|v\.?)$"}},
            {"LOWER": {"REGEX": r"^(christus|chr\.?)$"}}
        ]
    },
    { 
        "label": "DATESUFFIX", 
        "language": "nl",
        "pattern": [
            {"OP": "?", "LOWER": "år"},
            {"LOWER": "före"},
            {"LOWER": "nutid"}
        ]
    }
]