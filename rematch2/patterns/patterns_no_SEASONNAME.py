patterns_no_SEASONNAME = [
    { 
        "label": "SEASONNAME", 
        "comment": "spring",
        "language": "no",
        "pattern": [
            {"OP": "?", "LOWER": "på"},   
            {"LOWER": {"REGEX": r"^vår(en)?$"}}, 
            {"OP": "?", "LOWER": "i"}          
        ]
    },
    { 
        "label": "SEASONNAME",
        "comment": "summer", 
        "language": "no",
        "pattern": [
            {"OP": "?", "LOWER": "på"},   
            {"LOWER": {"REGEX": r"^sommer(en)?$"}}             
        ]
    },
    { 
        "label": "SEASONNAME", 
        "comment": "autumn",
        "language": "no",
        "pattern": [
            {"OP": "?", "LOWER": "på"},   
            {"LOWER": {"REGEX": r"^høst(en)?$"}}             
        ]
    },
    { 
        "label": "SEASONNAME", 
        "comment": "winter",
        "language": "no",
        "pattern": [
            {"OP": "?", "LOWER": "på"},   
            {"LOWER": {"REGEX": r"^vinter(en)?$"}}             
        ]
    },
    { 
        "label": "SEASONNAME",
        "comment": "dark time",
        "language": "no",
        "pattern": [
            {"LOWER": "mørketiden"}             
        ]
    },
    { 
        "label": "SEASONNAME", 
        "comment": "winter half",
        "language": "no",
        "pattern": [
            {"OP": "?", "LOWER": "på"},   
            {"LOWER": "vinterhalvåret"}             
        ]
    },
    { 
        "label": "SEASONNAME",
        "comment": "summer half", 
        "language": "no",
        "pattern": [
            {"OP": "?", "LOWER": "på"},   
            {"LOWER": "sommerhalvåret"}             
        ]
    }
]