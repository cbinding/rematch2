patterns_es_DATEPREFIX = [
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(hacia|aprox(\.|imadamente)?)$"}}
        ]
    },
    {
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(principios|inicio|mediales|finales)$"}}, 
            {"LOWER": {"REGEX": r"^del?"}}             
        ]
    },        
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(primera|segunda)$"}},
            {"LOWER": "mitad"},
            {"LOWER": {"REGEX": r"^del?"}}        
        ]
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(primer|segundo|tercer|cuarto)$"}},
            {"LOWER": "cuarto"},
            {"LOWER": {"REGEX": r"^del?"}} 
        ]
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(de|antes|durante|post|después|hasta|para)$"}},
            {"OP": "?", "LOWER": {"REGEX": r"^del?"}} 
        ]
    }
]