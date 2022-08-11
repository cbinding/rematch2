patterns_fr_DATEPREFIX = [
    { 
        "label": "DATEPREFIX", 
        "language": "fr",
        "comment": "start of, middle of, end of",
        "pattern": [
            {"LOWER": {"REGEX": r"^(d[eé]but|milieu|fin)$"}},
            {"OP": "?", "LOWER": {"REGEX": r"^d[eu]$"}}
        ]
    },
    { 
        "label": "DATEPREFIX", 
        "language": "fr",
        "comment": "beginning of the, middle of the, end of the",
        "pattern": [
            {"LOWER": {"REGEX": r"^(d[eé]but|milieu|fin)$"}},
            {"LOWER": "de"},
            {"LOWER": "la"}
        ]
    },
    { 
        "label": "DATEPREFIX", 
        "language": "fr",
        "comment": "during the",
        "pattern": [
            {"LOWER": "durant"},
            {"OP": "?", "LOWER": {"REGEX": r"^l[ea]$"}}
        ]
    },
    { 
        "label": "DATEPREFIX", 
        "language": "fr",
        "comment": "first/second half of",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": r"^(premi[eè]re|seconde|deuxi[eè]me)$"}},
            {"LOWER": {"REGEX": r"^moiti[eé]$"}},
            {"LOWER": "du"}
        ]
    },
    { 
        "label": "DATEPREFIX", 
        "language": "fr",
        "pattern": [
            {"LOWER": "durant"},
            {"LOWER": "tout"},
            {"LOWER": {"REGEX": r"^l[ea]$"}}
        ]
    },
    { 
        "label": "DATEPREFIX", 
        "language": "fr",
        "pattern": [
            {"LOWER": "au"},
            {"LOWER": "cours"},
            {"LOWER": "du"}
        ]
    },
    { 
        "label": "DATEPREFIX", 
        "language": "fr",
        "pattern": [
            {"LOWER": "au"},
            {"LOWER": "cours"},
            {"LOWER": "de"},
            {"LOWER": "la"}
        ]
    },
    { 
        "label": "DATEPREFIX", 
        "language": "fr",
        "pattern": [
            {"LOWER": "entre"},
            {"LOWER": "le"}
        ]
    },
    { 
        "label": "DATEPREFIX", 
        "language": "fr",
        "pattern": [
            {"LOWER": "à"},
            {"LOWER": "partir"},
            {"LOWER": "du"}
        ]
    },
    { 
        "label": "DATEPREFIX", 
        "language": "fr",
        "pattern": [
            {"LOWER": "à"},
            {"LOWER": "partir"},
            {"LOWER": "de"},
            {"LOWER": "la"}
        ]
    }
]