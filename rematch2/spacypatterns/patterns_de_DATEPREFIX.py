"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_de_DATEPREFIX.py
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
patterns_de_DATEPREFIX = [
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(ca?\.?|zirca|um|etwa)$"}}            
        ]
    },
    {
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(frühe|späte)[ns]$"}}            
        ]
    },  
    {
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(mitte|ende)$"}},          
            {"LOWER": "des"}            
        ]
    },      
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(erste|zweiten?)$"}},
            {"LOWER": "hälfte"},
            {"LOWER": "des"}            
        ]
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(erstes|zweites|drittes|viertes|letztes)$"}},
            {"LOWER": "viertel"},
            {"LOWER": "des"}            
        ]
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(anfang|vor|im|wurde|nach|seit|bis|ab|von|aus)$"}}
        ]
    }
]