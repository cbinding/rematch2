patterns_it_DATEPREFIX = [
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(c\.|circa)$"}},
            {"OP": "?", "LOWER": {"REGEX": r"^(al|ca.?)$"}}           
        ]
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(intorno|fino)$"}},
            {"LOWER": {"REGEX": r"^a(l'?)?$"}}           
        ]
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(inizio|fine)$"}},
            {"LOWER": {"REGEX": r"^del(l'?)?$"}}           
        ]
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(prima|tarda)$"}},
            {"LOWER": "età"}          
        ]
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(prim[io]|medio|mezzo)$"}} 
        ]
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"OP": "?", "ENT_TYPE": "ORDINAL"}, 
            {"LOWER": "metà"},
            {"LOWER": "del"}
        ]
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(medio|mezzo)$"}} 
        ]
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"ENT_TYPE": "ORDINAL"}, 
            {"LOWER": {"REGEX": r"^(quarto|trimestre)$"}}, 
            {"OP": "?", "LOWER": "del"}
        ]
    }
]