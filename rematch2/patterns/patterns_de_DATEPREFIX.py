patterns_de_DATEPREFIX = [
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(ca?\.?|zirca|um|etwa)$"}}            
        ]
    },
    {
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(frühe|späte)[ns]$"}}            
        ]
    },  
    {
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(mitte|ende)$"}},          
            {"LOWER": "des"}            
        ]
    },      
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(erste|zweiten?)$"}},
            {"LOWER": "hälfte"},
            {"LOWER": "des"}            
        ]
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(erstes|zweites|drittes|viertes|letztes)$"}},
            {"LOWER": "viertel"},
            {"LOWER": "des"}            
        ]
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(anfang|vor|im|wurde|nach|seit|bis|ab|von|aus)$"}}
        ]
    }
]