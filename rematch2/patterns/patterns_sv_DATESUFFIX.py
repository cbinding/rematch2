patterns_sv_DATESUFFIX = [
    { 
        "label": "DATESUFFIX", 
        "language": "sv",
        "pattern": [
            {"LOWER": {"REGEX": r"^(efter|enligt|före)$"}},
            {"LOWER": "vår"},
            {"LOWER": "tideräkning"}
        ]
    },  
    { 
        "label": "DATESUFFIX", 
        "language": "sv",
        "pattern": [
            {"LOWER": {"REGEX": r"^[ef]\.?v\.?t\.?$"}}            
        ]
    },  
    { 
        "label": "DATESUFFIX", 
        "language": "sv",
        "pattern": [
            {"LOWER": {"REGEX": r"^(efter|e\.?|före|f\.?)$"}},
            {"LOWER": {"REGEX": r"^(kristus|kr\.?|k\.?)$"}}
        ]
    },  
    { 
        "label": "DATESUFFIX", 
        "language": "sv",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": r"^cal\.?$"}},
            {"LOWER": {"REGEX": r"^(a\.?c\.?|b\.?p\.?|b\.?c\.?(e\.?)?)$"}}
        ]
    },
    { 
        "label": "DATESUFFIX", 
        "language": "sv",
        "pattern": [
            {"LOWER": "före"},
            {"LOWER": "nutid"}
        ]
    }
]