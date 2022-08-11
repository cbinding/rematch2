patterns_es_DATESUFFIX = [
    { 
        "label": "DATESUFFIX",
        "comment": "ad | bc | bce | bp | ce | a.d. | b.c. | b.c.e. | b.p. | c.e.",
        "language": "es",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": r"cal\.?"}},
            {"LOWER": {"REGEX": r"^(ad|bce?|bp|ce|a\.d\.|b\.c\.(e\.)?|b\.p\.|c\.e\.)$"}}
        ]
    },
    { 
        "label": "DATESUFFIX",
        "comment": "de cristo | antes de cristo",
        "language": "es",
        "pattern": [
            {"OP": "?", "LOWER": "antes"},
            {"LOWER": "de"},
            {"LOWER": "cristo"}
        ]
    }
]