patterns_no_SEASONNAME = [
    { 
        "label": "SEASONNAME", 
        "comment": "spring",
		"pattern": [
            {"OP": "?", "LOWER": "på"},   
            {"LOWER": {"REGEX": r"^vår(en)?$"}}, 
            {"OP": "?", "LOWER": "i"}          
        ]
    },
    { 
        "label": "SEASONNAME",
        "comment": "summer",
		"pattern": [
            {"OP": "?", "LOWER": "på"},   
            {"LOWER": {"REGEX": r"^sommer(en)?$"}}             
        ]
    },
    { 
        "label": "SEASONNAME", 
        "comment": "autumn",
		"pattern": [
            {"OP": "?", "LOWER": "på"},   
            {"LOWER": {"REGEX": r"^høst(en)?$"}}             
        ]
    },
    { 
        "label": "SEASONNAME", 
        "comment": "winter",
		"pattern": [
            {"OP": "?", "LOWER": "på"},   
            {"LOWER": {"REGEX": r"^vinter(en)?$"}}             
        ]
    },
    { 
        "label": "SEASONNAME",
        "comment": "dark time",
		"pattern": [
            {"LOWER": "mørketiden"}             
        ]
    },
    { 
        "label": "SEASONNAME", 
        "comment": "winter half",
		"pattern": [
            {"OP": "?", "LOWER": "på"},   
            {"LOWER": "vinterhalvåret"}             
        ]
    },
    { 
        "label": "SEASONNAME",
        "comment": "summer half",
		"pattern": [
            {"OP": "?", "LOWER": "på"},   
            {"LOWER": "sommerhalvåret"}             
        ]
    }
]