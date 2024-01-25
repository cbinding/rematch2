"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_es_DATESUFFIX.py
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
patterns_es_DATESUFFIX = [
    { 
        # "ac | dc | ad | bc | bce | bp | ce | a.c. | d.c. | a.d. | b.c. | b.c.e. | b.p. | c.e."
        "label": "DATESUFFIX",
		"pattern": [
            {"OP": "?", "LOWER": {"REGEX": r"cal\.?"}},
            {"LOWER": {"REGEX": r"^(ac|dc|ad|bce?|bp|ce|a\.c\.|d\.c\.|a\.d\.|b\.c\.(e\.)?|b\.p\.|c\.e\.)$"}}
        ]
    },
    { 
        # "a. C. | d. C."
        "label": "DATESUFFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^[ad]\.$"}},
            {"LOWER": "c."}
        ]
    },
    { 
        # "de cristo" | "antes de cristo"
        "label": "DATESUFFIX",
		"pattern": [
            {"OP": "?", "LOWER": "antes"},
            {"LOWER": "de"},
            {"LOWER": "cristo"}
        ]
    }
]