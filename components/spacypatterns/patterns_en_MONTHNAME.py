"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_en_MONTHNAME.py
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
patterns_en_MONTHNAME = [
    { 
        # Jan
        "id": "http://vocab.getty.edu/aat/300410290",
        "label": "MONTHNAME",
		"pattern": [
            {"POS": "PROPN", "LOWER": {"REGEX": r"^(jan(uary|\.)?)$"}}            
        ]
    },
    { 
        # Feb
        "id": "http://vocab.getty.edu/aat/300410291",
        "label": "MONTHNAME",
		"pattern": [
            {"POS": "PROPN", "LOWER": {"REGEX": r"^(feb(ruary|\.)?)$"}}            
        ]
    },
    { 
        # Mar
        "id": "http://vocab.getty.edu/aat/300410292",
        "label": "MONTHNAME",
		"pattern": [
            {"POS": "PROPN", "LOWER": {"REGEX": r"^(mar(ch|\.)?)$"}}            
        ]
    },
    { 
        # Apr
        "id": "http://vocab.getty.edu/aat/300410293",
        "label": "MONTHNAME",
		"pattern": [
            {"POS": "PROPN", "LOWER": {"REGEX": r"^(apr(il|\.)?)$"}}            
        ]
    },
    { 
        # May
        "id": "http://vocab.getty.edu/aat/300410294",
        "label": "MONTHNAME",
		"pattern": [
            {"POS": "PROPN", "LOWER": "may"}            
        ]
    },
    { 
        # Jun
        "id": "http://vocab.getty.edu/aat/300410295",
        "label": "MONTHNAME",
		"pattern": [
            {"POS": "PROPN", "LOWER": {"REGEX": r"^(jun(e|\.)?)$"}}            
        ]
    },
    { 
        # Jul
        "id": "http://vocab.getty.edu/aat/300410296",
        "label": "MONTHNAME",
		"pattern": [
            {"POS": "PROPN", "LOWER": {"REGEX": r"^(jul(y|\.)?)$"}}            
        ]
    },
    { 
        # Aug
        "id": "http://vocab.getty.edu/aat/300410297",
        "label": "MONTHNAME",
		"pattern": [
            {"POS": "PROPN", "LOWER": {"REGEX": r"^(aug(ust|\.)?)$"}}            
        ]
    },
    { 
        # Sep
        "id": "http://vocab.getty.edu/aat/300410298",
        "label": "MONTHNAME",
		"pattern": [
            {"POS": "PROPN", "LOWER": {"REGEX": r"^(sep(t\.?|tember|\.)?)$"}}            
        ]
    },
    { 
        # Oct
        "id": "http://vocab.getty.edu/aat/300410299",
        "label": "MONTHNAME",
		"pattern": [
            {"POS": "PROPN", "LOWER": {"REGEX": r"^(oct(ober|\.)?)$"}}            
        ]
    },
    { 
        # Nov
        "id": "http://vocab.getty.edu/aat/300410300",
        "label": "MONTHNAME",
		"pattern": [
            {"POS": "PROPN", "LOWER": {"REGEX": r"^(nov(ember|\.)?)$"}}            
        ]
    },
    { 
        # Dec
        "id": "http://vocab.getty.edu/aat/300410301",
        "label": "MONTHNAME",
		"pattern": [
            {"POS": "PROPN", "LOWER": {"REGEX": r"^(dec(ember|\.)?)$"}}            
        ]
    }
]