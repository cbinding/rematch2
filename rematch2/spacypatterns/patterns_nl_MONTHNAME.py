patterns_nl_MONTHNAME = [
    { 
        # Jan
        "id": "http://vocab.getty.edu/aat/300410290",
        "label": "MONTHNAME", 
        "comment": "jan | jan. | januari",
		"pattern": [
            {"LOWER": {"REGEX": r"^jan(\.|uari)?$"}}            
        ]
    },
    { 
        # Feb
        "id": "http://vocab.getty.edu/aat/300410291",
        "label": "MONTHNAME", 
        "comment": "feb | feb. | februari",
		"pattern": [
            {"LOWER": {"REGEX": r"^feb(\.|ruari)?$"}}            
        ]
    },
    { 
        # Mar
        "id": "http://vocab.getty.edu/aat/300410292",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": "maart"}            
        ]
    },
    { 
        # Apr
        "id": "http://vocab.getty.edu/aat/300410293",
        "label": "MONTHNAME",
        "comment": "apr | apr. | april",
		"pattern": [
            {"LOWER": {"REGEX": r"^apr(\.|il)?$"}}            
        ]
    },
    { 
        # May
        "id": "http://vocab.getty.edu/aat/300410294",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": "mei"}            
        ]
    },
    { 
        # Jun
        "id": "http://vocab.getty.edu/aat/300410295",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": "juni"}            
        ]
    },
    { 
        # Jul
        "id": "http://vocab.getty.edu/aat/300410296",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": "juli"}            
        ]
    },
    { 
        # Aug
        "id": "http://vocab.getty.edu/aat/300410297",
        "label": "MONTHNAME",
        "comment": "aug | aug. | augustus",
		"pattern": [
            {"LOWER": {"REGEX": r"^aug(\.|ustus)?$"}}            
        ]
    },
    { 
        # Sep
        "id": "http://vocab.getty.edu/aat/300410298",
        "label": "MONTHNAME", 
        "comment": "sept | sept. | september",
		"pattern": [
            {"LOWER": {"REGEX": r"^sept(\.|ember)?$"}}            
        ]
    },
    { 
        # Oct
        "id": "http://vocab.getty.edu/aat/300410299",
        "label": "MONTHNAME",
        "comment": "oct | oct. | okt | okt. |october | oktober",
		"pattern": [
            {"LOWER": {"REGEX": r"^o[kc]t(\.|ober)?$"}}            
        ]
    },
    { 
        # Nov
        "id": "http://vocab.getty.edu/aat/300410300",
        "label": "MONTHNAME",
        "comment": "nov | nov. | november",
		"pattern": [
            {"LOWER": {"REGEX": r"^nov(\.|ember)?$"}}            
        ]
    },
    { 
        # Nov
        "id": "http://vocab.getty.edu/aat/300410301",
        "label": "MONTHNAME", 
        "comment": "dec | dec. | december",
		"pattern": [
            {"LOWER": {"REGEX": r"^dec(\.|ember)?$"}}            
        ]
    }
]