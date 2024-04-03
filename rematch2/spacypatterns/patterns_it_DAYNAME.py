"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_it_DAYNAME.py
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
patterns_it_DAYNAME = [
    { 
        "id": "http://vocab.getty.edu/aat/300410304",
        "label": "DAYNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^lun(\.|edì)?$"}}            
        ]
    },
    { 
        "id": "http://vocab.getty.edu/aat/300410305",
        "label": "DAYNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^mar(\.|tedì)?$"}}            
        ]
    },
    { 
        "id": "http://vocab.getty.edu/aat/300410306",
        "label": "DAYNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"mer(\.|coledì)?$"}}           
        ]
    },
    { 
        "id": "http://vocab.getty.edu/aat/300410307",
        "label": "DAYNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^gio(\.|vedì)?$"}}            
        ]
    },
    { 
        "id": "http://vocab.getty.edu/aat/300410308",
        "label": "DAYNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^ven(\.|erdì)?$"}}            
        ]
    },
    { 
        "id": "http://vocab.getty.edu/aat/300410309",
        "label": "DAYNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^sab(\.|ato)?$"}}           
        ]
    },
    { 
        "id": "http://vocab.getty.edu/aat/300410310",
        "label": "DAYNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^do(\.|menica)?$"}}            
        ]
    }
]