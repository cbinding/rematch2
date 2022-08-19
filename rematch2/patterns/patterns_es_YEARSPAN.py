patterns_es_YEARSPAN = [
    { 
        "label": "YEARSPAN", 
        
        "comment": "e.g. start of March 1715 AD",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "MONTHNAME"},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"} 
        ]
    },
    { 
        "label": "YEARSPAN", 
        
        "comment": "e.g. mid autumn 1715 AD",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "SEASONNAME"},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"} 
        ]
    },
    { 
        "label": "YEARSPAN", 
        
        "comment": "e.g. mid 1580 AD",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "+", "ENT_TYPE": "DATESUFFIX"}
        ] 
    },
    { 
        "label": "YEARSPAN", 
        
        "comment": "",
		"pattern": [
            {"ORTH": {"REGEX": r"^\d+[\–\-/]\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ] 
    },
    { 
        "label": "YEARSPAN", 
        
        "comment": "",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}, 
            {"ENT_TYPE": "DATESEPARATOR"}, 
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ] 
    }
]