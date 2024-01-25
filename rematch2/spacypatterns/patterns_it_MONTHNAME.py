"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_it_MONTHNAME.py
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
patterns_it_MONTHNAME = [
    { 
        # Jan
        "id": "http://vocab.getty.edu/aat/300410290",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^genn(?:\.|aio)?$"}}            
        ]
    },
    { 
        # Feb
        "id": "http://vocab.getty.edu/aat/300410291",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^febbr(?:\.|aio)?$"}}            
        ]
    },
    { 
        # Mar
        "id": "http://vocab.getty.edu/aat/300410292",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^mar(?:\.|zo)?$"}}            
        ]
    },
    { 
        # Apr
        "id": "http://vocab.getty.edu/aat/300410293",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^apr(?:\.|ile)?$"}}            
        ]
    },
    { 
        # May
        "id": "http://vocab.getty.edu/aat/300410294",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^magg(?:\.|io)?$"}}            
        ]
    },
    { 
        # Jun
        "id": "http://vocab.getty.edu/aat/300410295",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^giu(?:\.|gno)?$"}}            
        ]
    },
    { 
        # Jul
        "id": "http://vocab.getty.edu/aat/300410296",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^lug(?:\.|lio)?$"}}            
        ]
    },
    { 
        # Aug
        "id": "http://vocab.getty.edu/aat/300410297",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^ag(?:\.|osto)?$"}}            
        ]
    },
    { 
        # Sep
        "id": "http://vocab.getty.edu/aat/300410298",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^sett(?:\.|embre)?$"}}            
        ]
    },
    { 
        # Oct
        "id": "http://vocab.getty.edu/aat/300410299",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^ott(?:\.|obre)?$"}}            
        ]
    },
    { 
        # Nov
        "id": "http://vocab.getty.edu/aat/300410300",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^nov(?:\.|embre)?$"}}            
        ]
    },
    { 
        # Dec
        "id": "http://vocab.getty.edu/aat/300410301",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^dic(?:\.|embre)$"}}            
        ]
    }
]