patterns_cy_DATEPREFIX = [
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(ca?\.?|circa|oddeuta|tua\'r)$"}}            
        ]
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": "o"},  
            {"LOWER": "gwmpas"}          
        ]
    },
    {
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": "hanner"},
            {"LOWER": "cyntaf"},
            {"OP": "?", "LOWER": "y"}            
        ]
    },
    {
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": "canol"}, 
            {"OP": "?", "LOWER": "y"}            
        ]
    }
]