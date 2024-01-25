"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_es_DAYNAME.py
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
patterns_es_DAYNAME = [
    { 
        "id": "http://vocab.getty.edu/aat/300410304",
        "label": "DAYNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^lun(es)?$"}}            
        ]
    },
    { 
        "id": "http://vocab.getty.edu/aat/300410305",
        "label": "DAYNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^mar(tes)?$"}}            
        ]
    },
    { 
        "id": "http://vocab.getty.edu/aat/300410306",
        "label": "DAYNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^mi[eé](rcoles)?$"}}           
        ]
    },
    { 
        "id": "http://vocab.getty.edu/aat/300410307",
        "label": "DAYNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^jue(ves)?$"}}            
        ]
    },
    { 
        "id": "http://vocab.getty.edu/aat/300410308",
        "label": "DAYNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^vie(rnes)?$"}}            
        ]
    },
    { 
        "id": "http://vocab.getty.edu/aat/300410309",
        "label": "DAYNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^sáb(ado)?$"}}           
        ]
    },
    { 
        "id": "http://vocab.getty.edu/aat/300410310",
        "label": "DAYNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^dom(ingo)?$"}}            
        ]
    }
]