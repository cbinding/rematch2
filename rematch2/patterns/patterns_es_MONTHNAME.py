patterns_es_MONTHNAME = [
    { 
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": "enero"}            
        ]
    },
    { 
        "label": "MONTHNAME",
        "comment": "feb | feb. | febrero",
		"pattern": [
            {"LOWER": {"REGEX": r"^feb(\.|rero)?$"}}            
        ]
    },
    { 
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": "marzo"}            
        ]
    },
    { 
        "label": "MONTHNAME", 
        "comment": "abr | abr. | abril",
		"pattern": [
            {"LOWER": {"REGEX": r"^abr(?:\.|il)?$"}}            
        ]
    },
    { 
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": "mayo"}            
        ]
    },
    { 
        "label": "MONTHNAME", 
        "comment": "jun | jun. | junio",
		"pattern": [
            {"LOWER": {"REGEX": r"^jun(?:\.|io)?$"}}            
        ]
    },
    { 
        "label": "MONTHNAME", 
        "comment": "jul | jul. | julio",
		"pattern": [
            {"LOWER": {"REGEX": r"^jul(?:\.|io)?$"}}            
        ]
    },
    { 
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": "agosto"}            
        ]
    },
    { 
        "label": "MONTHNAME", 
        "comment": "sept | sept. | septiembre",
		"pattern": [
            {"LOWER": {"REGEX": r"^sept(\.|iembre)?$"}}            
        ]
    },
    { 
        "label": "MONTHNAME",
        "comment": "oct | oct. | octubre",
		"pattern": [
            {"LOWER": {"REGEX": r"^oct(\.|ubre)?$"}}            
        ]
    },
    { 
        "label": "MONTHNAME", 
        "comment": "nov | nov. | noviembre",
		"pattern": [
            {"LOWER": {"REGEX": r"^nov(?:\.|iembre)?$"}}            
        ]
    },
    { 
        "label": "MONTHNAME", 
        "comment": "dic | dic. | diciembre",
		"pattern": [
            {"LOWER": {"REGEX": r"^dic(?:\.|iembre)?$"}}            
        ]
    }
]