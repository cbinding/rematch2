"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_sv_ORDINAL.py
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
patterns_sv_ORDINAL = [
    { 
        "label": "ORDINAL",
		"pattern": [
           {"LOWER": {"IN": [
                "första", "andra", "tredje", "fjärde", "femte",
                "sjätte", "sjunde", "åttonde", "nionde", "tionde",
                "elfte", "tolfte", "trettonde", "fjortonde", "femtonde",
                "sextonde", "sjuttonde", "artonde", "nittonde", "tjugonde",
                "tjugoförsta","tjugoandra","tjugotredje","tjugofjärde","tjugofemte",
                "tjugosjätte", "tjugosjunde", "tjugoåttonde", "tjugonionde", 
                "trettionde", "trettioförsta"
            ]}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^\d+[ae]$"}}            
        ] 
    }
]