patterns_sv_CENTURY = [
    { 
        "label": "CENTURY",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"LOWER": {"REGEX": r"^\d+00\-(talet)?$"}},  
            {"ENT_TYPE": "DATESEPARATOR"}, 
            {"LOWER": {"REGEX": r"^\d+00\-(talet)?$"}},    
            {"OP": "?", "ENT_TYPE": "DATESUFFIX"}      
        ] 
    },
    { 
        "label": "CENTURY", 
        
        "comment": "",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "ORDINAL"},
            {"LOWER": {"REGEX": r"^(århundradet|årtusendet)$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"} 
        ]
    },
    { 
        "label": "CENTURY", 
        
        "comment": "",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "ORDINAL"},
            {"OP": "?", "LOWER": {"REGEX": r"^(århundradet|årtusendet)$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"},
            {"ENT_TYPE": "DATESEPARATOR"},
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "ORDINAL"},
            {"LOWER": {"REGEX": r"^(århundradet|årtusendet)$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"} 
        ]
    }
]