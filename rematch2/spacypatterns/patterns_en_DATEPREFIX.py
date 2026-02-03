"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_en_DATEPREFIX.py
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
patterns_en_DATEPREFIX = [
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(circa|around|approximately)$"}}            
        ]
    },
    {
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(beginning|start|middle|end)$"}},
            {"LOWER": "of"},
            {"OP": "?", "LOWER":"the"}
        ]
    },    
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(first|second|1st|2nd)$"}},
            {"LOWER": "half"},
            {"LOWER": "of"},
            {"OP": "?", "LOWER": "the"}
        ]
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(first|second|third|fourth|last|1st|2nd|3rd|4th|final)$"}},
            {"LOWER": "quarter"},
            {"LOWER": "of"},
            {"OP": "?", "LOWER": "the"}
        ]
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": "during"},
            {"OP": "?", "LOWER": "the"}
        ]
    },
    {
        "label": "DATEPREFIX",
        "comment": "early|earlier|lower|mid|middle|upper|high|late|later",
		"pattern": [
            {"LOWER": {"REGEX": r"^(earl(y|ier)|lower|mid(dle)?|upper|high|later?)$"}}
        ]
    }
]