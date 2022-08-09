patterns_es_MONTHNAME = [
    { 
        "label": "MONTHNAME", 
        "language": "es",
        "pattern": [
            {"LOWER": "enero"}            
        ]
    },
    { 
        "label": "MONTHNAME",
        "comment": "feb | feb. | febrero", 
        "language": "es",        
        "pattern": [
            {"LOWER": {"REGEX": r"^feb(\.|rero)?$"}}            
        ]
    },
    { 
        "label": "MONTHNAME", 
        "language": "es",
        "pattern": [
            {"LOWER": "marzo"}            
        ]
    },
    { 
        "label": "MONTHNAME", 
        "comment": "abr | abr. | abril",
        "language": "es",
        "pattern": [
            {"LOWER": {"REGEX": r"^abr(?:\.|il)?$"}}            
        ]
    },
    { 
        "label": "MONTHNAME", 
        "language": "es",
        "pattern": [
            {"LOWER": "mayo"}            
        ]
    },
    { 
        "label": "MONTHNAME", 
        "comment": "jun | jun. | junio",
        "language": "es",
        "pattern": [
            {"LOWER": {"REGEX": r"^jun(?:\.|io)?$"}}            
        ]
    },
    { 
        "label": "MONTHNAME", 
        "comment": "jul | jul. | julio",
        "language": "es",
        "pattern": [
            {"LOWER": {"REGEX": r"^jul(?:\.|io)?$"}}            
        ]
    },
    { 
        "label": "MONTHNAME", 
        "language": "es",
        "pattern": [
            {"LOWER": "agosto"}            
        ]
    },
    { 
        "label": "MONTHNAME", 
        "comment": "sept | sept. | septiembre",
        "language": "es",
        "pattern": [
            {"LOWER": {"REGEX": r"^sept(\.|iembre)?$"}}            
        ]
    },
    { 
        "label": "MONTHNAME",
        "comment": "oct | oct. | octubre",
        "language": "es",
        "pattern": [
            {"LOWER": {"REGEX": r"^oct(\.|ubre)?$"}}            
        ]
    },
    { 
        "label": "MONTHNAME", 
        "comment": "nov | nov. | noviembre",
        "language": "es",
        "pattern": [
            {"LOWER": {"REGEX": r"^nov(?:\.|iembre)?$"}}            
        ]
    },
    { 
        "label": "MONTHNAME", 
        "comment": "dic | dic. | diciembre",
        "language": "es",
        "pattern": [
            {"LOWER": {"REGEX": r"^dic(?:\.|iembre)?$"}}            
        ]
    }
]