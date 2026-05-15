"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_sv_DATEPREFIX.py
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
patterns_sv_DATEPREFIX = [
    { 
        "label": "DATEPREFIX",
        "comment": "circa | ungefär | runt | tidigt",
		"pattern": [
            {"LOWER": {"REGEX": r"^(?:circa|ungefär|runt|tidigt)$"}}
        ] 
    }, 
    { 
        "label": "DATEPREFIX",
        "comment": "början av | början av det | mitten av | mitten av det | slutet av | slutet av det",
		"pattern": [
            {"LOWER": {"REGEX": r"^(?:början|mitten|slutet)$"}},
            {"LOWER": "av"},
            {"OP": "?", "LOWER": "det"}
        ] 
    },   
    { 
        "label": "DATEPREFIX",
        "comment": "sen | sent | sena | sentida",
		"pattern": [
            {"LOWER": {"REGEX": r"^(sen[ta]?|sentida)$"}}
        ] 
    }, 
    { 
        "label": "DATEPREFIX",
        "comment": "första hälften | första hälften av | första hälften av det",
		"pattern": [
            {"LOWER": "första"},
            {"LOWER": "hälften"},
            {"OP": "?", "LOWER": "av"},
            {"OP": "?", "LOWER": "det"}
        ] 
    },
    { 
        "label": "DATEPREFIX",
        "comment": "andra halvan | andra halvan av | första hälften av det",
		"pattern": [
            {"LOWER": "andra"},
            {"LOWER": "halvan"},
            {"OP": "?", "LOWER": "av"},
            {"OP": "?", "LOWER": "det"}
        ] 
    },    
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(första|andra|tredje|fjärde$)"}},
            {"LOWER": "kvartalet"},
            {"OP": "?", "LOWER": "av"},
            {"OP": "?", "LOWER": "det"}
        ] 
    }        
]