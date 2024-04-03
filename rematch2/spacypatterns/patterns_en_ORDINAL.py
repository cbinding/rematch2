"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_en_ORDINAL.py
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
patterns_en_ORDINAL = [
    { 
        "label": "ORDINAL",
		"pattern": [
           {"LOWER": {"IN": [
                "first","second","third","fourth","fifth",
                "sixth","seventh","eighth","ninth","tenth",
                "eleventh","twelfth","thirteenth","fourteenth","fifteenth",
                "sixteenth","seventeenth","eighteenth","nineteenth","twentieth" 
            ]}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^\d+(st|nd|rd|th)$"}}            
        ] 
    }
]