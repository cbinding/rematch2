patterns_cy_DATEPREFIX = [
    { 
        "label": "DATEPREFIX", 
        "language": "cy",
        "pattern": [
            {"LOWER": {"REGEX": r"^(ca?\.?|circa|oddeuta|tua\'r)$"}}            
        ]
    },
    { 
        "label": "DATEPREFIX", 
        "language": "cy",
        "pattern": [
            {"LOWER": "o"},  
            {"LOWER": "gwmpas"}          
        ]
    },
    {
        "label": "DATEPREFIX", 
        "language": "cy",
        "pattern": [
            {"LOWER": "hanner"},
            {"LOWER": "cyntaf"},
            {"OP": "?", "LOWER": "y"}            
        ]
    },
    {
        "label": "DATEPREFIX", 
        "language": "cy",
        "pattern": [
            {"LOWER": "canol"}, 
            {"OP": "?", "LOWER": "y"}            
        ]
    }
]