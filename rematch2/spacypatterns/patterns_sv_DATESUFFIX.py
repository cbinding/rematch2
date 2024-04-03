"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_sv_DATESUFFIX.py
Version :   20240125
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy patterns for use with SpanRuler pipeline components            
Imports :   
Example :           
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
History :   25/01/2024 CFB Initially created script
=============================================================================
"""
patterns_sv_DATESUFFIX = [
    { 
        "label": "DATESUFFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(efter|enligt|före)$"}},
            {"LOWER": "vår"},
            {"LOWER": "tideräkning"}
        ]
    },  
    { 
        "label": "DATESUFFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^[ef]\.?v\.?t\.?$"}}            
        ]
    },  
    { 
        "label": "DATESUFFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(efter|e\.?|före|f\.?)$"}},
            {"LOWER": {"REGEX": r"^(kristus|kr\.?|k\.?)$"}}
        ]
    },  
    { 
        "label": "DATESUFFIX",
		"pattern": [
            {"OP": "?", "LOWER": {"REGEX": r"^cal\.?$"}},
            {"LOWER": {"REGEX": r"^(a\.?c\.?|b\.?p\.?|b\.?c\.?(e\.?)?)$"}}
        ]
    },
    { 
        "label": "DATESUFFIX",
		"pattern": [
            {"LOWER": "före"},
            {"LOWER": "nutid"}
        ]
    }
]