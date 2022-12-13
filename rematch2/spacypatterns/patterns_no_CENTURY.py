patterns_no_CENTURY = [
    { 
        "label": "CENTURY",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"LOWER": {"REGEX": r"^\d+00\-tallets?$"}},            
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}            
        ]
    },
    { 
        "label": "CENTURY",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ENT_TYPE": "ORDINAL"},
            {"LOWER": {"REGEX": r"^(århundre|årtusen)$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}            
        ]
    },
    { 
        "label": "CENTURY",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ENT_TYPE": "ORDINAL"},
            {"OP": "?", "LOWER": {"REGEX": r"^(?:århundre|årtusen)$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"},
            {"ENT_TYPE": "DATESEPARATOR"},
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ENT_TYPE": "ORDINAL"},
            {"LOWER": {"REGEX": r"^(?:århundre|årtusen)$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ]
    }
]