patterns_it_DATEPREFIX = [
    { 
        "label": "DATEPREFIX", 
        "language": "it",
        "pattern": [
            {"LOWER": {"REGEX": r"^(c\.|circa)$"}},
            {"OP": "?", "LOWER": {"REGEX": r"^(al|ca.?)$"}}           
        ]
    },
    { 
        "label": "DATEPREFIX", 
        "language": "it",
        "pattern": [
            {"LOWER": {"REGEX": r"^(intorno|fino)$"}},
            {"LOWER": {"REGEX": r"^a(l'?)?$"}}           
        ]
    },
    { 
        "label": "DATEPREFIX", 
        "language": "it",
        "pattern": [
            {"LOWER": {"REGEX": r"^(inizio|fine)$"}},
            {"LOWER": {"REGEX": r"^del(l'?)?$"}}           
        ]
    },
    { 
        "label": "DATEPREFIX", 
        "language": "it",
        "pattern": [
            {"LOWER": {"REGEX": r"^(prima|tarda)$"}},
            {"LOWER": "età"}          
        ]
    },
    { 
        "label": "DATEPREFIX", 
        "language": "it",
        "pattern": [
            {"LOWER": {"REGEX": r"^(prim[io]|medio|mezzo)$"}} 
        ]
    },
    { 
        "label": "DATEPREFIX", 
        "language": "it",
        "pattern": [
            {"OP": "?", "ENT_TYPE": "ORDINAL"}, 
            {"LOWER": "metà"},
            {"LOWER": "del"}
        ]
    },
    { 
        "label": "DATEPREFIX", 
        "language": "it",
        "pattern": [
            {"LOWER": {"REGEX": r"^(medio|mezzo)$"}} 
        ]
    },
    { 
        "label": "DATEPREFIX", 
        "language": "it",
        "pattern": [
            {"ENT_TYPE": "ORDINAL"}, 
            {"LOWER": {"REGEX": r"^(quarto|trimestre)$"}}, 
            {"OP": "?", "LOWER": "del"}
        ]
    }
]