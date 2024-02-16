"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_en_CENTURY.py
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
patterns_en_CENTURY = [
    { 
        "label": "CENTURY",         
        "comment": "e.g. beginning of the fifth century AD",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "ORDINAL"},
            {"LOWER": {"REGEX": r"^(century|centuries|millennium)$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"} 
        ]
    },
    { 
        "label": "CENTURY",         
        "comment": "e.g. start of the first to end of the 2nd century AD",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "ORDINAL"},
            {"OP": "?", "LOWER": {"REGEX": r"^(century|centuries|millennium)$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"},
            {"ENT_TYPE": "DATESEPARATOR"},
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "ORDINAL"},
            {"LOWER": {"REGEX": r"^(century|centuries|millennium)$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"} 
        ]
    }
]