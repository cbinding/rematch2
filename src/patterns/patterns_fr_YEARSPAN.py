patterns_fr_YEARSPAN = [        
    { 
        "label": "YEARSPAN", 
        "language": "fr",
        "comment": "",
        "pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "MONTHNAME"},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"} 
        ]
    },
    { 
        "label": "YEARSPAN", 
        "language": "fr",
        "comment": "",
        "pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "SEASONNAME"},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"} 
        ]
    },
    { 
        "label": "YEARSPAN", 
        "language": "fr",
        "comment": "",
        "pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "+", "ENT_TYPE": "DATESUFFIX"}
        ] 
    },
    { 
        "label": "YEARSPAN", 
        "language": "fr",
        "comment": "",
        "pattern": [
            {"ORTH": {"REGEX": r"^\d+[\–\-/]\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ] 
    },
    { 
        "label": "YEARSPAN", 
        "language": "fr",
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
    },
    { 
        "label": "YEARSPAN", 
        "language": "fr",
        "pattern": [ 
            {"OP": "?", "LOWER": {"REGEX": "^ann[eé]es?$"}},
            {"LOWER": {"REGEX": r"^\d+$"}}, 
            {"ENT_TYPE": "DATESEPARATOR"},
            {"LOWER": {"REGEX": r"^\d+$"}} 
        ]
    },    
    { 
        "label": "YEARSPAN", 
        "language": "fr",
        "pattern": [ 
            {"LOWER": {"REGEX": r"^(ann[eé]es?|en)$"}},
            {"LOWER": {"REGEX": r"^\d+$"}}
        ]
    }
]