"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_no_DATESUFFIX.py
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
patterns_no_DATESUFFIX = [ 
    { 
        "label": "DATESUFFIX",
		"pattern": [
            {"OP": "?", "LOWER": {"REGEX": r"cal\.?"}},
            {"LOWER": {"REGEX": r"^(ad|bc|bce|bp|a\.d\.|b\.c\.|b\.c\.e\.|b\.p\.|[ef]\.kr\.)$"}}              
        ]
    },
    { 
        "label": "DATESUFFIX",
		"pattern": [
            {"LOWER": "cal"},
            {"OP": "?", "LOWER": "."},
            {"LOWER": {"REGEX": r"^(b[cp])$"}} 
        ]
    },
    { 
        "label": "DATESUFFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^[ef]\.$"}},
            {"LOWER": {"REGEX": r"^kr\.?$"}}                 
        ]
    }
]