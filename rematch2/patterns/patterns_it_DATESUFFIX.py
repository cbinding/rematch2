patterns_it_DATESUFFIX = [
    { 
        "label": "DATESUFFIX",
		"pattern": [            
            {"LOWER": {"REGEX": r"^(?:d\.?c\.?|c\.?e\.?)$"}}
        ]
    },
    { 
        "label": "DATESUFFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(?:a\.?c\.?|b\.?c\.?(?:e\.?)?)$"}}
        ]
    },
    { 
        "label": "DATESUFFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^b\.?p\.?$"}}
        ]
    }
]