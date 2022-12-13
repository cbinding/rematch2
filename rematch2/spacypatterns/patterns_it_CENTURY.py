patterns_it_CENTURY = [
    { 
        "label": "CENTURY",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "ORDINAL"},
            {"LOWER": {"REGEX": r"^(sec(olo|\.)|mill(ennio|\.))$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"} 
        ]
    },
    { 
        "label": "CENTURY",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"TEXT": {"REGEX": r"[MCDLXVI]+"}}, 
            {"LOWER": {"REGEX": r"^(sec(olo|\.)|mill(ennio|\.))$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"} 
        ]
    },
    { 
        "label": "CENTURY",
		"pattern": [
            {"TEXT": {"REGEX": r"[MCDLXVI]+\-[MCDLXVI]+"}}, 
            {"LOWER": {"REGEX": r"^(sec(olo|\.)|mill(ennio|\.))$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"} 
        ]
    },
    { 
        "label": "CENTURY",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "ORDINAL"},
            {"OP": "?", "LOWER": {"REGEX": r"^(sec(olo|\.)|mill(ennio|\.))$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"},
            {"ENT_TYPE": "DATESEPARATOR"},
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "ORDINAL"},
            {"LOWER": {"REGEX": r"^(sec(olo|\.)|mill(ennio|\.))$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"} 
        ]
    },
    { 
        "label": "CENTURY",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "ORDINAL"},
            {"LOWER": {"REGEX": r"^(sec(olo|\.)|mill(ennio|\.))$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"},
            {"ENT_TYPE": "DATESEPARATOR"},
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "ORDINAL"},
            {"OP": "?", "LOWER": {"REGEX": r"^(sec(olo|\.)|mill(ennio|\.))$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"} 
        ]
    }
]