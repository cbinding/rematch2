"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_es_DATEPREFIX.py
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
patterns_es_DATEPREFIX = [
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(hacia|aprox(\.|imadamente)?)$"}}
        ]
    },
    {
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(principios|inicio|mediales|finales)$"}}, 
            {"LOWER": {"REGEX": r"^del?"}}             
        ]
    },        
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(primera|segunda)$"}},
            {"LOWER": "mitad"},
            {"LOWER": {"REGEX": r"^del?"}}        
        ]
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(primer|segundo|tercer|cuarto)$"}},
            {"LOWER": "cuarto"},
            {"LOWER": {"REGEX": r"^del?"}} 
        ]
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(de|antes|durante|post|después|hasta|para)$"}},
            {"OP": "?", "LOWER": {"REGEX": r"^del?"}} 
        ]
    }
]