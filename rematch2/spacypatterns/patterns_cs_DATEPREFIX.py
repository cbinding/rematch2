"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_cs_DATEPREFIX.py
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
patterns_cs_DATEPREFIX = [
    { 
        # circa
        "id": "circa",
        "label": "DATEPREFIX",
        "pattern": "cca"
    },
    {
        # early
        "id": "early",
        "label": "DATEPREFIX",
        "pattern": "počátek"		
    },  
    {
        # mid
        "id": "mid",
        "label": "DATEPREFIX",
        "pattern": "polovina"	
    },      
    { 
        # late
        "id": "late",
        "label": "DATEPREFIX",
        "pattern": "konec"
    },
    { 
        # first half
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(1\.|první)$"}},
            {"LOWER": "polovina"}            
        ]
    },
    { 
        # second half
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(2\.|druhá)$"}},
            {"LOWER": "polovina"}            
        ]
    },
    { 
        # first quarter
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(1\.|první)$"}},
            {"LOWER": "čtvrtina"}            
        ]
    },
    { 
        # second quarter
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(2\.|druhá)$"}},
            {"LOWER": "čtvrtina"}            
        ]
    },
    { 
        # third quarter
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(3\.|třetí)$"}},
            {"LOWER": "čtvrtina"}            
        ]
    },
    { 
        # fourth quarter
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(4\.|čtvrtá)$"}},
            {"LOWER": "čtvrtina"}            
        ]
    }
]