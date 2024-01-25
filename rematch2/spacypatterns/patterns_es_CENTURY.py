"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_es_CENTURY.py
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
patterns_es_CENTURY = [
    { 
        "label": "CENTURY",
		"pattern": [
            {"LOWER": {"REGEX": r"^(siglos?|milenios?)$"}},
            {"TEXT": {"REGEX": r"[MCDLXVI]+\-[MCDLXVI]+"}}, 
            {"OP": "?", "ENT_TYPE": "DATESUFFIX"} 
        ]
    },
    { 
        "label": "CENTURY",         
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
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"LOWER": {"REGEX": r"^(siglos|milenio)$"}},
            {"ENT_TYPE": "ORDINAL"},            
            {"OP": "?", "ENT_TYPE": "DATESUFFIX"},
            {"ENT_TYPE": "DATESEPARATOR"},
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"OP": "?", "LOWER": {"REGEX": r"^(siglos|milenio)$"}}, 
            {"ENT_TYPE": "ORDINAL"},            
            {"OP": "?", "ENT_TYPE": "DATESUFFIX"} 
        ]
    },
    { 
        "label": "CENTURY",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"OP": "?", "LOWER": {"REGEX": r"^(siglos?|milenio)$"}},
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