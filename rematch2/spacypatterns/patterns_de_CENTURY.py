patterns_de_CENTURY = [
    { 
        "label": "CENTURY",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "ORDINAL"},
            {"LOWER": {"REGEX": r"^(jahrhunderts?|jhs?\.?|jahrtausends?)$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"} 
        ]
    },
    { 
        "label": "CENTURY",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "ORDINAL"},
            {"OP": "?", "LOWER": {"REGEX": r"^(jahrhunderts?|jhs?\.?|jahrtausends?)$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"},
            {"ENT_TYPE": "DATESEPARATOR"},
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "ORDINAL"},
            {"LOWER": {"REGEX": r"^(jahrhunderts?|jhs?\.?|jahrtausends?)$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"} 
        ]
    }
]