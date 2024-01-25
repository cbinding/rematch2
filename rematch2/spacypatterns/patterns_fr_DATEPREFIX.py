"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_fr_DATEPREFIX.py
Version :   20240125
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy patterns for use with EntityRuler pipeline components            
Imports :   
Example :           
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
History :   25/01/2024 CFB Initially created script
=============================================================================
"""
patterns_fr_DATEPREFIX = [
    { 
        "label": "DATEPREFIX", 
        
        "comment": "start of, middle of, end of",
		"pattern": [
            {"LOWER": {"REGEX": r"^(d[eé]but|milieu|fin)$"}},
            {"OP": "?", "LOWER": {"REGEX": r"^d[eu]$"}}
        ]
    },
    { 
        "label": "DATEPREFIX", 
        
        "comment": "beginning of the, middle of the, end of the",
		"pattern": [
            {"LOWER": {"REGEX": r"^(d[eé]but|milieu|fin)$"}},
            {"LOWER": "de"},
            {"LOWER": "la"}
        ]
    },
    { 
        "label": "DATEPREFIX", 
        
        "comment": "during the",
		"pattern": [
            {"LOWER": "durant"},
            {"OP": "?", "LOWER": {"REGEX": r"^l[ea]$"}}
        ]
    },
    { 
        "label": "DATEPREFIX", 
        
        "comment": "first/second half of",
		"pattern": [
            {"OP": "?", "LOWER": {"REGEX": r"^(premi[eè]re|seconde|deuxi[eè]me)$"}},
            {"LOWER": {"REGEX": r"^moiti[eé]$"}},
            {"LOWER": "du"}
        ]
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": "durant"},
            {"LOWER": "tout"},
            {"LOWER": {"REGEX": r"^l[ea]$"}}
        ]
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": "au"},
            {"LOWER": "cours"},
            {"LOWER": "du"}
        ]
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": "au"},
            {"LOWER": "cours"},
            {"LOWER": "de"},
            {"LOWER": "la"}
        ]
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": "entre"},
            {"LOWER": "le"}
        ]
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": "à"},
            {"LOWER": "partir"},
            {"LOWER": "du"}
        ]
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": "à"},
            {"LOWER": "partir"},
            {"LOWER": "de"},
            {"LOWER": "la"}
        ]
    }
]