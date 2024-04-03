"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_it_DATEPREFIX.py
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
patterns_it_DATEPREFIX = [
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(c\.|circa)$"}},
            {"OP": "?", "LOWER": {"REGEX": r"^(al|ca.?)$"}}           
        ]
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(intorno|fino)$"}},
            {"LOWER": {"REGEX": r"^a(l'?)?$"}}           
        ]
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(inizio|fine)$"}},
            {"LOWER": {"REGEX": r"^del(l'?)?$"}}           
        ]
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(prima|tarda)$"}},
            {"LOWER": "età"}          
        ]
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(prim[io]|medio|mezzo)$"}} 
        ]
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"_": {"is_ordinal": True}},
            {"LOWER": "metà"},
            {"LOWER": "del"}
        ]
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(medio|mezzo)$"}} 
        ]
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"_": {"is_ordinal": True}},
            {"LOWER": {"REGEX": r"^(quarto|trimestre)$"}}, 
            {"OP": "?", "LOWER": "del"}
        ]
    }
]