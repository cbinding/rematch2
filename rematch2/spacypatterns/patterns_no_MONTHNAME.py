"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_no_MONTHNAME.py
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
patterns_no_MONTHNAME = [
    { 
        # Jan
        "id": "http://vocab.getty.edu/aat/300410290",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^jan(uar)?$"}}            
        ]
    },
    { 
        # Feb
        "id": "http://vocab.getty.edu/aat/300410291",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^feb(r|ruar)?$"}}            
        ]
    },
    { 
        # Mar
        "id": "http://vocab.getty.edu/aat/300410292",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^mars?$"}}            
        ]
    },
    { 
        # Apr
        "id": "http://vocab.getty.edu/aat/300410293",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^apr(il)?$"}}            
        ]
    },
    { 
        # May
        "id": "http://vocab.getty.edu/aat/300410294",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^mai$"}}            
        ]
    },
    { 
        # Jun
        "id": "http://vocab.getty.edu/aat/300410295",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^juni?$"}}            
        ]
    },
    { 
        # Jul
        "id": "http://vocab.getty.edu/aat/300410296",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^juli?$"}}            
        ]
    },
    { 
        # Aug
        "id": "http://vocab.getty.edu/aat/300410297",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^aug(ust)?$"}}            
        ]
    },
    { 
        # Sep
        "id": "http://vocab.getty.edu/aat/300410298",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^sept(ember)?$"}}            
        ]
    },
    { 
        # Oct
        "id": "http://vocab.getty.edu/aat/300410299",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^okt(ober)?$"}}            
        ]
    },
    { 
        # Nov
        "id": "http://vocab.getty.edu/aat/300410300",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^nov(ember)?$"}}            
        ]
    },
    { 
        # Dec
        "id": "http://vocab.getty.edu/aat/300410301",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^des(ember)?$"}}            
        ]
    }
]