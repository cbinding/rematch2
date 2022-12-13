patterns_no_DATESUFFIX = [ 
    { 
        "label": "DATESUFFIX",
		"pattern": [
            {"OP": "?", "LOWER": {"REGEX": r"cal\.?"}},
            {"LOWER": {"REGEX": r"^(ad|bc|bce|bp|a\.d\.|b\.c\.|b\.c\.e\.|b\.p\.|[ef]\.kr\.)$"}}              
        ]
    },
    { 
        "label": "DATESUFFIX",
		"pattern": [
            {"LOWER": "cal"},
            {"OP": "?", "LOWER": "."},
            {"LOWER": {"REGEX": r"^(b[cp])$"}} 
        ]
    },
    { 
        "label": "DATESUFFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^[ef]\.$"}},
            {"LOWER": {"REGEX": r"^kr\.?$"}}                 
        ]
    }
]