patterns_en_DATESUFFIX = [
    { 
        "label": "DATESUFFIX",
        "comment": "ad | bc | bce | bp | ce | a.d. | b.c. | b.c.e. | b.p. | c.e.",
        "language": "en",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": r"cal\.?"}},
            {"LOWER": {"REGEX": r"^(ad|bce?|bp|ce|a\.d\.|b\.c\.(e\.)?|b\.p\.|c\.e\.)$"}}
        ]
    }
]