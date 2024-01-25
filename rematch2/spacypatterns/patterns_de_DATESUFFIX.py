"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_de_DATESUFFIX.py
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
patterns_de_DATESUFFIX = [
    { 
        "label": "DATESUFFIX",
        "comment": "ad | bc | bce | bp | ce | a.d. | b.c. | b.c.e. | b.p. | c.e.",
		"pattern": [
            {"LOWER": {"REGEX": r"^(ad|bce?|bp|ce|a\.d\.|b\.c\.(e\.)?|b\.p\.|c\.e\.)$"}}
        ]
    },
    { 
        "label": "DATESUFFIX",
        "comment": "n chr | n. chr. | na christus",
		"pattern": [
            {"LOWER": {"REGEX": r"^n(\.|a\.?)?$"}},
            {"LOWER": {"REGEX": r"^chr(\.|istus)?$"}}
        ]
    },
    { 
        "label": "DATESUFFIX",
        "comment": "v chr | v. chr. | vor christus",
		"pattern": [
            {"LOWER": {"REGEX": r"^v(\.|or\.?)?$"}},
            {"LOWER": {"REGEX": r"^chr(\.|istus)?$"}}
        ]
    }
]