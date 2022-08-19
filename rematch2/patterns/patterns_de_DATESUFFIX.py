patterns_de_DATESUFFIX = [
    { 
        "label": "DATESUFFIX",
        "comment": "ad | bc | bce | bp | ce | a.d. | b.c. | b.c.e. | b.p. | c.e.",
		"pattern": [
            {"LOWER": {"REGEX": r"^(ad|bce?|bp|ce|a\.d\.|b\.c\.(e\.)?|b\.p\.|c\.e\.)$"}}
        ]
    },
    { 
        "label": "DATESUFFIX",
        "comment": "n chr | n. chr. | na christus",
		"pattern": [
            {"LOWER": {"REGEX": r"^n(\.|a\.?)?$"}},
            {"LOWER": {"REGEX": r"^chr(\.|istus)?$"}}
        ]
    },
    { 
        "label": "DATESUFFIX",
        "comment": "v chr | v. chr. | vor christus",
		"pattern": [
            {"LOWER": {"REGEX": r"^v(\.|or\.?)?$"}},
            {"LOWER": {"REGEX": r"^chr(\.|istus)?$"}}
        ]
    }
]