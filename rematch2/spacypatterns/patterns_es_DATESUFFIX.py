patterns_es_DATESUFFIX = [
    { 
        # "ac | dc | ad | bc | bce | bp | ce | a.c. | d.c. | a.d. | b.c. | b.c.e. | b.p. | c.e."
        "label": "DATESUFFIX",
		"pattern": [
            {"OP": "?", "LOWER": {"REGEX": r"cal\.?"}},
            {"LOWER": {"REGEX": r"^(ac|dc|ad|bce?|bp|ce|a\.c\.|d\.c\.|a\.d\.|b\.c\.(e\.)?|b\.p\.|c\.e\.)$"}}
        ]
    },
    { 
        # "a. C. | d. C."
        "label": "DATESUFFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^[ad]\.$"}},
            {"LOWER": "c."}
        ]
    },
    { 
        # "de cristo" | "antes de cristo"
        "label": "DATESUFFIX",
		"pattern": [
            {"OP": "?", "LOWER": "antes"},
            {"LOWER": "de"},
            {"LOWER": "cristo"}
        ]
    }
]