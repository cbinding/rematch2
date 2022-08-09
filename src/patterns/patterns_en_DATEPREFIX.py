patterns_en_DATEPREFIX = [
    { 
        "label": "DATEPREFIX", 
        "language": "en",
        "pattern": [
            {"LOWER": {"REGEX": r"^(c\.|circa|around|approximately)$"}}            
        ]
    },
    {
        "label": "DATEPREFIX", 
        "language": "en",
        "pattern": [
            {"LOWER": {"REGEX": r"^(beginning|start|middle|end)$"}},
            {"LOWER": "of"},
            {"OP": "?", "LOWER":"the"}
        ]
    },    
    { 
        "label": "DATEPREFIX",
        "language": "en", 
        "pattern": [
            {"LOWER": {"REGEX": r"^(first|second|1st|2nd)$"}},
            {"LOWER": "half"},
            {"LOWER": "of"},
            {"OP": "?", "LOWER": "the"}
        ]
    },
    { 
        "label": "DATEPREFIX", 
        "language": "en",
        "pattern": [
            {"LOWER": {"REGEX": r"^(first|second|third|fourth|last|1st|2nd|3rd|4th|final)$"}},
            {"LOWER": "quarter"},
            {"LOWER": "of"},
            {"OP": "?", "LOWER": "the"}
        ]
    },
    { 
        "label": "DATEPREFIX", 
        "language": "en",
        "pattern": [
            {"LOWER": "during"},
            {"OP": "?", "LOWER": "the"}
        ]
    },
    {
        "label": "DATEPREFIX",
        "comment": "early|earlier|lower|mid|middle|upper|late|later",
        "language": "en", 
        "pattern": [
            {"LOWER": {"REGEX": r"^(earl(y|ier)|lower|mid(dle)?|upper|later?)$"}}
        ]
    }
]