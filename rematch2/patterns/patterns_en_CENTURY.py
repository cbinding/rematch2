patterns_en_CENTURY = [
    { 
        "label": "CENTURY", 
        
        "comment": "e.g. beginning of the fifth century AD",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "ORDINAL"},
            {"LOWER": {"REGEX": r"^(century|centuries|millennium)$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"} 
        ]
    },
    { 
        "label": "CENTURY", 
        
        "comment": "e.g. start of the first to end of the 2nd century AD",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "ORDINAL"},
            {"OP": "?", "LOWER": {"REGEX": r"^(century|centuries|millennium)$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"},
            {"ENT_TYPE": "DATESEPARATOR"},
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "ORDINAL"},
            {"LOWER": {"REGEX": r"^(century|centuries|millennium)$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"} 
        ]
    }
]