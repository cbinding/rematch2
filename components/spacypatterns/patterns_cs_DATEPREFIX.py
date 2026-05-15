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
        "pattern": [
            {"LOWER": {"REGEX": r"^polovin[yaě]$"}}
        ]
    },      
    { 
        # late
        "id": "late",
        "label": "DATEPREFIX",
        "pattern": "konec"
    },
    { 
        # late
        "id": "early",
        "label": "DATEPREFIX",
        "pattern": "na konci"
    },
    { 
        # during the
        "id": "during",
        "label": "DATEPREFIX",
        "pattern": "v průběhu"
    },
     { 
        # at the turn of the
        "id": "during",
        "label": "DATEPREFIX",
        "pattern": "na přelomu"
    },    
    { 
        # first half / first quarter
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(1\.|první)$"}},
            {"LOWER": {"REGEX": r"^(polovin[yaě]|čtvrtin[yaě])$"}}           
        ]
    },
    { 
        # first half / first quarter
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^[12]$"}},
            {"TEXT": {"REGEX": r"^\."}},
            {"LOWER": {"REGEX": r"^(polovin[yaě]|čtvrtin[yaě])$"}}           
        ]
    },
    { 
        # second half / second quarter
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(2\.|druhá)$"}},
            {"LOWER": {"REGEX": r"^(polovin[yaě]|čtvrtin[yaě])$"}}            
        ]
    },    
    { 
        # third quarter
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(3\.|třetí)$"}},
            {"LOWER": {"REGEX": r"^čtvrtin[yaě]$"}} 
        ]
    },
    { 
        # fourth quarter
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(4\.|čtvrtá)$"}},
            {"LOWER": {"REGEX": r"^čtvrtin[yaě]$"}}        
        ]
    },
    { 
        # quarters
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^[1234]$"}},
            {"TEXT": {"REGEX": r"^\."}},
            {"LOWER": "čtvrtina"}           
        ]
    },
]