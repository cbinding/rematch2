"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_en_DAYNAME.py
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
patterns_en_DAYNAME = [
    { 
        "id": "http://vocab.getty.edu/aat/300410304",
        "label": "DAYNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^mon(\.|day)?$"}}            
        ]
    },
    { 
        "id": "http://vocab.getty.edu/aat/300410305",
        "label": "DAYNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^tues(\.|day)?$"}}            
        ]
    },
    { 
        "id": "http://vocab.getty.edu/aat/300410306",
        "label": "DAYNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^wed(\.|nesday)?$"}}           
        ]
    },
    { 
        "id": "http://vocab.getty.edu/aat/300410307",
        "label": "DAYNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^thu(r?\.?|rsday)?$"}}            
        ]
    },
    { 
        "id": "http://vocab.getty.edu/aat/300410308",
        "label": "DAYNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^fri(\.|day)?$"}}            
        ]
    },
    { 
        "id": "http://vocab.getty.edu/aat/300410309",
        "label": "DAYNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^sat(\.|urday)?$"}}           
        ]
    },
    { 
        "id": "http://vocab.getty.edu/aat/300410310",
        "label": "DAYNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^sun(\.|day)?$"}}            
        ]
    }
]