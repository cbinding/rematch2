patterns_fr_YEARSPAN = [        
    { 
        "label": "YEARSPAN",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "MONTHNAME"},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"} 
        ]
    },
    { 
        "label": "YEARSPAN",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "SEASONNAME"},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"} 
        ]
    },
    { 
        "label": "YEARSPAN",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "+", "ENT_TYPE": "DATESUFFIX"}
        ] 
    },
    { 
        "label": "YEARSPAN",
		"pattern": [
            {"ORTH": {"REGEX": r"^\d+[\–\-/]\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ] 
    },
    { 
        "label": "YEARSPAN",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}, 
            {"ENT_TYPE": "DATESEPARATOR"},
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ] 
    },
    { 
        "label": "YEARSPAN",
		"pattern": [ 
            {"OP": "?", "LOWER": {"REGEX": "^ann[eé]es?$"}},
            {"LOWER": {"REGEX": r"^\d+$"}}, 
            {"ENT_TYPE": "DATESEPARATOR"},
            {"LOWER": {"REGEX": r"^\d+$"}} 
        ]
    },    
    { 
        "label": "YEARSPAN",
		"pattern": [ 
            {"LOWER": {"REGEX": r"^(ann[eé]es?|en)$"}},
            {"LOWER": {"REGEX": r"^\d+$"}}
        ]
    }
]