"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_nl_DAYNAME.py
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
patterns_nl_DAYNAME = [
    {
        "id": "http://vocab.getty.edu/aat/300410304", 
        "label": "DAYNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^ma(\.|andag)?$"}}            
        ]
    },
    { 
        "id": "http://vocab.getty.edu/aat/300410305", 
        "label": "DAYNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^di(\.|nsdag)?$"}}            
        ]
    },
    { 
        "id": "http://vocab.getty.edu/aat/300410306", 
        "label": "DAYNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^woe(\.|nsdag)?$"}}           
        ]
    },
    { 
        "id": "http://vocab.getty.edu/aat/300410307", 
        "label": "DAYNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^don(\.|derdag)?$"}}            
        ]
    },
    { 
        "id": "http://vocab.getty.edu/aat/300410308", 
        "label": "DAYNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^vrij(\.|dag)?$"}}            
        ]
    },
    {
        "id": "http://vocab.getty.edu/aat/300410309",  
        "label": "DAYNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^zat(\.|erdag)?$"}}           
        ]
    },
    {
        "id": "http://vocab.getty.edu/aat/300410310",  
        "label": "DAYNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^zon(\.|dag)?$"}}            
        ]
    }
]