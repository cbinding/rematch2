patterns_es_CENTURY = [
    { 
        "label": "CENTURY", 
        "language": "es",
        "comment": "",
        "pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"LOWER": {"REGEX": r"^(siglo|milenio)$"}},
            {"ENT_TYPE": "ORDINAL"},            
            {"OP": "?", "ENT_TYPE": "DATESUFFIX"} 
        ]
    },
    { 
        "label": "CENTURY", 
        "language": "es",
        "comment": "",
        "pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"OP": "?", "LOWER": {"REGEX": r"^(siglo|milenio)$"}},
            {"ENT_TYPE": "ORDINAL"},            
            {"OP": "?", "ENT_TYPE": "DATESUFFIX"},
            {"ENT_TYPE": "DATESEPARATOR"},
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"LOWER": {"REGEX": r"^(siglo|milenio)$"}},
            {"ENT_TYPE": "ORDINAL"},            
            {"OP": "?", "ENT_TYPE": "DATESUFFIX"} 
        ]
    }
]