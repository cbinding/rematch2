patterns_fr_CENTURY = [
    { 
        "label": "CENTURY",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "ORDINAL"},
            {"LOWER": {"REGEX": r"^s((\.|i[eè]cle)?|mill[eé]naire)$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"} 
        ]
    },
    { 
        "label": "CENTURY",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "ORDINAL"},
            {"OP": "?", "LOWER": {"REGEX": r"^s((\.|i[eè]cle)?|mill[eé]naire)$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"},
            {"ENT_TYPE": "DATESEPARATOR"},
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "ORDINAL"},
            {"LOWER": {"REGEX": r"^s((\.|i[eè]cle)?|mill[eé]naire)$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"} 
        ]
    },
    { 
        "label": "CENTURY",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "ORDINAL"},
            {"LOWER": {"REGEX": r"^s((\.|i[eè]cle)?|mill[eé]naire)$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"},
            {"ENT_TYPE": "DATESEPARATOR"},
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "ORDINAL"},
            {"OP": "?", "LOWER": {"REGEX": r"^s((\.|i[eè]cle)?|mill[eé]naire)$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"} 
        ]
    }    
]
