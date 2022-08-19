patterns_es_CENTURY = [
    { 
        "label": "CENTURY",
		"pattern": [
            {"LOWER": {"REGEX": r"^(siglos?|milenios?)$"}},
            {"TEXT": {"REGEX": r"[MCDLXVI]+\-[MCDLXVI]+"}}, 
            {"OP": "?", "ENT_TYPE": "DATESUFFIX"} 
        ]
    },
    { 
        "label": "CENTURY",         
        "comment": "",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"LOWER": {"REGEX": r"^(siglo|milenio)$"}},
            {"ENT_TYPE": "ORDINAL"},            
            {"OP": "?", "ENT_TYPE": "DATESUFFIX"} 
        ]
    },
    { 
        "label": "CENTURY",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"LOWER": {"REGEX": r"^(siglos|milenio)$"}},
            {"ENT_TYPE": "ORDINAL"},            
            {"OP": "?", "ENT_TYPE": "DATESUFFIX"},
            {"ENT_TYPE": "DATESEPARATOR"},
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"OP": "?", "LOWER": {"REGEX": r"^(siglos|milenio)$"}}, 
            {"ENT_TYPE": "ORDINAL"},            
            {"OP": "?", "ENT_TYPE": "DATESUFFIX"} 
        ]
    },
    { 
        "label": "CENTURY",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"OP": "?", "LOWER": {"REGEX": r"^(siglos?|milenio)$"}},
            {"ENT_TYPE": "ORDINAL"},            
            {"OP": "?", "ENT_TYPE": "DATESUFFIX"},
            {"ENT_TYPE": "DATESEPARATOR"},
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"LOWER": {"REGEX": r"^(siglo|milenio)$"}}, 
            {"ENT_TYPE": "ORDINAL"},            
            {"OP": "?", "ENT_TYPE": "DATESUFFIX"} 
        ]
    }
]