patterns_no_YEARSPAN = [
    { 
        "label": "YEARSPAN", 
        "language": "no",
        "pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "MONTHNAME"},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"} 
        ]
    },
    { 
        "label": "YEARSPAN", 
        "language": "no",
        "pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "SEASONNAME"},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"} 
        ]
    },    
    { 
        "label": "YEARSPAN", 
        "language": "no",
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
        "language": "no",
        "pattern": [
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"ORTH": {"REGEX": r"^\\p{pD}$"}},
            {"ORTH": {"REGEX": r"^\d+$"}}            
        ] 
    },
    { 
        "label": "YEARSPAN", 
        "language": "no",
        "pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ORTH": {"REGEX": r"^\d+±\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"},
            {"ENT_TYPE": "DATESEPARATOR"},
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ORTH": {"REGEX": r"^\d+±\d+$"}},   
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}         
        ] 
    },   
    { 
        "label": "YEARSPAN", 
        "language": "no",
        "pattern": [
            {"LOWER": {"REGEX": r"^\d+±\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}                  
        ] 
    },
    { 
        "label": "YEARSPAN", 
        "language": "no",
        "pattern": [
            {"LOWER": {"REGEX": r"^\d+$"}},
            {"LOWER": {"REGEX": r"^(bp)?±\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}                  
        ] 
    },    
    { 
        "label": "YEARSPAN", 
        "language": "no",
        "pattern": [
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "+", "ENT_TYPE": "DATESUFFIX"}                  
        ] 
    }
]