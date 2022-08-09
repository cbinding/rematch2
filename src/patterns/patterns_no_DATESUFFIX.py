patterns_no_DATESUFFIX = [ 
    { 
        "label": "DATESUFFIX", 
        "language": "no",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": r"cal\.?"}},
            {"LOWER": {"REGEX": r"^(ad|bc|bce|bp|a\.d\.|b\.c\.|b\.c\.e\.|b\.p\.|[ef]\.kr\.)$"}}              
        ]
    },
    { 
        "label": "DATESUFFIX", 
        "language": "no",
        "pattern": [
            {"LOWER": "cal"},
            {"OP": "?", "LOWER": "."},
            {"LOWER": {"REGEX": r"^(b[cp])$"}} 
        ]
    },
    { 
        "label": "DATESUFFIX", 
        "language": "no",
        "pattern": [
            {"LOWER": {"REGEX": r"^[ef]\.$"}},
            {"LOWER": {"REGEX": r"^kr\.?$"}}                 
        ]
    }
]