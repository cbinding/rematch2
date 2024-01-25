"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_fr_MONTHNAME.py
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
patterns_fr_MONTHNAME = [
    { 
        # Jan
        "id": "http://vocab.getty.edu/aat/300410290",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^janv(?:\.|ier)?$"}}            
        ]
    },
    { 
        # Feb
        "id": "http://vocab.getty.edu/aat/300410291",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^févr(?:\.|ier)?$"}}            
        ]
    },
    { 
        # Mar
        "id": "http://vocab.getty.edu/aat/300410292",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": "mars"}            
        ]
    },
    { 
        # Apr
        "id": "http://vocab.getty.edu/aat/300410293",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^avr(?:\.|il)?$"}}            
        ]
    },
    { 
        # May
        "id": "http://vocab.getty.edu/aat/300410294",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": "mai"}            
        ]
    },
    { 
        # Jun
        "id": "http://vocab.getty.edu/aat/300410295",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": "juin"}            
        ]
    },
    { 
        # Jul
        "id": "http://vocab.getty.edu/aat/300410296",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^juill(?:\.|et)?$"}}            
        ]
    },
    { 
        # Aug
        "id": "http://vocab.getty.edu/aat/300410297",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": "août"}            
        ]
    },
    { 
        # Sep
        "id": "http://vocab.getty.edu/aat/300410298",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^sept(?:\.|embre)?$"}}            
        ]
    },
    { 
        # Oct
        "id": "http://vocab.getty.edu/aat/300410299",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^(oct(ober|\.)?)$"}}            
        ]
    },
    { 
        # Nov
        "id": "http://vocab.getty.edu/aat/300410300",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^oct(?:\.|obre)?$"}}            
        ]
    },
    { 
        # Dec
        "id": "http://vocab.getty.edu/aat/300410301",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^déc(?:\.|embre)?$"}}            
        ]
    }
]