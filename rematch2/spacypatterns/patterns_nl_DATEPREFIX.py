"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_nl_DATEPREFIX.py
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
patterns_nl_DATEPREFIX = [
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(ca\.?|ongeveer)$"}}            
        ]
    },
    {
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(vroege?|begin|midden|eind|laat|late)$"}}            
        ]
    },    
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(eerste|tweede)$"}},
            {"LOWER": "helft"}
        ]
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(eerste|tweede|derde|vierde)$"}},
            {"LOWER": {"REGEX": r"kwart(ier|aal)?"}}           
        ]
    }    
]