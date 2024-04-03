"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_cy_DAYNAME.py
Version :   20221027
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy patterns for use with SpanRuler pipeline components            
Imports :   
Example :           
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
History :   27/10/2022 CFB Initially created script
=============================================================================
"""
patterns_cy_DAYNAME = [
    { 
        "id": "http://vocab.getty.edu/aat/300410304",
        "label": "DAYNAME",
		"pattern": [
            { "OP": "?", "LOWER": { "REGEX": r"^(dd?|n)ydd$" } },
            { "LOWER": "llun" }            
        ]
    },
    { 
        "id": "http://vocab.getty.edu/aat/300410305",
        "label": "DAYNAME",
		"pattern": [
            { "OP": "?", "LOWER": { "REGEX": r"^(dd?|n)ydd$" } },
            {"LOWER": {"REGEX": r"^[mf]awrth$"}}            
        ]
    },
    { 
        "id": "http://vocab.getty.edu/aat/300410306",
        "label": "DAYNAME",
		"pattern": [
            { "OP": "?", "LOWER": { "REGEX": r"^(dd?|n)ydd$" } },
            {"LOWER": {"REGEX": r"^[mf]ercher$"}}           
        ]
    },
    { 
        "id": "http://vocab.getty.edu/aat/300410307",
        "label": "DAYNAME",
		"pattern": [
            { "OP": "?", "LOWER": { "REGEX": r"^(dd?|n)ydd$" } },
            {"LOWER": "iau" }            
        ]
    },
    { 
        "id": "http://vocab.getty.edu/aat/300410308",
        "label": "DAYNAME",
		"pattern": [
            { "OP": "?", "LOWER": { "REGEX": r"^(dd?|n)ydd$" } },
            {"LOWER": {"REGEX": r"^(n?g)?wener$"}}            
        ]
    },
    { 
        "id": "http://vocab.getty.edu/aat/300410309",
        "label": "DAYNAME",
		"pattern": [
            { "OP": "?", "LOWER": { "REGEX": r"^(dd?|n)ydd$" } },
            { "LOWER": "sadwrn" }           
        ]
    },
    { 
        "id": "http://vocab.getty.edu/aat/300410310",
        "label": "DAYNAME",
		"pattern": [
            { "OP": "?", "LOWER": { "REGEX": r"^(dd?|n)ydd$" } },
            { "LOWER": "sul" }            
        ]
    }
]