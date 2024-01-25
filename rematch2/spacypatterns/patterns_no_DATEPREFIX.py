"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_no_DATEPREFIX.py
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
patterns_no_DATEPREFIX = [
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^cir[ck]a$"}}
        ] 
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^ca\.?$"}}
        ] 
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": "rundt"}
        ] 
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": "omtrent"}
        ] 
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(?:[eäæ]ldre|yngre|eldste|tidl?[ei]g)$"}},  
            {"OP": "?", "LOWER": {"REGEX": r"^på$"}}
        ] 
    },    
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": "inngangen"},  
            {"LOWER": "til"}           
        ] 
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(begynnelsen|slutten$)"}},  
            {"LOWER": "av"},
            {"OP": "?", "LOWER": "det"}
        ] 
    },    
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^f[oø]r$"}}
        ] 
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(?:i|på)$"}}
        ] 
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"OP": "?", "LOWER": "i"},
            {"LOWER": "løpet"},
            {"LOWER": "av"}                
        ] 
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(?:etter|siden)$"}}
        ] 
    }    
]