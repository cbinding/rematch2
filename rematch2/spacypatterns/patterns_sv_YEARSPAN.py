patterns_sv_YEARSPAN = [ 
        { 
        "label": "YEARSPAN",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"LOWER": {"REGEX": r"^\d+0\-talet$"}}             
        ] 
    },
    { 
        "label": "YEARSPAN", 
        
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
        
        "comment": "",
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
            {"ORTH": {"REGEX": r"^\d+[\–\-]\d+$"}},
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
    },
    { 
        "label": "YEARSPAN",
        "comment": "**See https://stackoverflow.com/questions/57477852/spacy-matcher-with-entities-spanning-more-than-a-single-token  retokenizing with custom entity types..",
		"pattern": [
           {"ORTH": "xxxxxxxxx"}
        ]
    }
]
