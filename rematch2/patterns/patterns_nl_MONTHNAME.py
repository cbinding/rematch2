patterns_nl_MONTHNAME = [
    { 
        "label": "MONTHNAME", 
        "comment": "jan | jan. | januari",
		"pattern": [
            {"LOWER": {"REGEX": r"^jan(\.|uari)?$"}}            
        ]
    },
    { 
        "label": "MONTHNAME", 
        "comment": "feb | feb. | februari",
		"pattern": [
            {"LOWER": {"REGEX": r"^feb(\.|ruari)?$"}}            
        ]
    },
    { 
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": "maart"}            
        ]
    },
    { 
        "label": "MONTHNAME",
        "comment": "apr | apr. | april",
		"pattern": [
            {"LOWER": {"REGEX": r"^apr(\.|il)?$"}}            
        ]
    },
    { 
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": "mei"}            
        ]
    },
    { 
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": "juni"}            
        ]
    },
    { 
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": "juli"}            
        ]
    },
    { 
        "label": "MONTHNAME",
        "comment": "aug | aug. | augustus",
		"pattern": [
            {"LOWER": {"REGEX": r"^aug(\.|ustus)?$"}}            
        ]
    },
    { 
        "label": "MONTHNAME", 
        "comment": "sept | sept. | september",
		"pattern": [
            {"LOWER": {"REGEX": r"^sept(\.|ember)?$"}}            
        ]
    },
    { 
        "label": "MONTHNAME",
        "comment": "oct | oct. | okt | okt. |october | oktober",
		"pattern": [
            {"LOWER": {"REGEX": r"^o[kc]t(\.|ober)?$"}}            
        ]
    },
    { 
        "label": "MONTHNAME",
        "comment": "nov | nov. | november",
		"pattern": [
            {"LOWER": {"REGEX": r"^nov(\.|ember)?$"}}            
        ]
    },
    { 
        "label": "MONTHNAME", 
        "comment": "dec | dec. | december",
		"pattern": [
            {"LOWER": {"REGEX": r"^dec(\.|ember)?$"}}            
        ]
    }
]