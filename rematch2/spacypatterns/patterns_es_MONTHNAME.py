"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_es_MONTHNAME.py
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
patterns_es_MONTHNAME = [
    { 
        # Jan
        "id": "http://vocab.getty.edu/aat/300410290",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": "enero"}            
        ]
    },
    { 
        # Feb
        "id": "http://vocab.getty.edu/aat/300410291",
        "label": "MONTHNAME",
        "comment": "feb | feb. | febrero",
		"pattern": [
            {"LOWER": {"REGEX": r"^feb(\.|rero)?$"}}            
        ]
    },
    { 
        # Mar
        "id": "http://vocab.getty.edu/aat/300410292",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": "marzo"}            
        ]
    },
    { 
        # Apr
        "id": "http://vocab.getty.edu/aat/300410293",
        "label": "MONTHNAME", 
        "comment": "abr | abr. | abril",
		"pattern": [
            {"LOWER": {"REGEX": r"^abr(?:\.|il)?$"}}            
        ]
    },
    { 
        # May
        "id": "http://vocab.getty.edu/aat/300410294",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": "mayo"}            
        ]
    },
    { 
        # Jun
        "id": "http://vocab.getty.edu/aat/300410295",
        "label": "MONTHNAME", 
        "comment": "jun | jun. | junio",
		"pattern": [
            {"LOWER": {"REGEX": r"^jun(?:\.|io)?$"}}            
        ]
    },
    { 
        # Jul
        "id": "http://vocab.getty.edu/aat/300410296",
        "label": "MONTHNAME", 
        "comment": "jul | jul. | julio",
		"pattern": [
            {"LOWER": {"REGEX": r"^jul(?:\.|io)?$"}}            
        ]
    },
    { 
        # Aug
        "id": "http://vocab.getty.edu/aat/300410297",
        "label": "MONTHNAME",
		"pattern": [
            {"LOWER": "agosto"}            
        ]
    },
    { 
        # Sep
        "id": "http://vocab.getty.edu/aat/300410298",
        "label": "MONTHNAME", 
        "comment": "sept | sept. | septiembre",
		"pattern": [
            {"LOWER": {"REGEX": r"^sept(\.|iembre)?$"}}            
        ]
    },
    { 
        # Oct
        "id": "http://vocab.getty.edu/aat/300410299",
        "label": "MONTHNAME",
        "comment": "oct | oct. | octubre",
		"pattern": [
            {"LOWER": {"REGEX": r"^oct(\.|ubre)?$"}}            
        ]
    },
    { 
        # Nov
        "id": "http://vocab.getty.edu/aat/300410300",
        "label": "MONTHNAME", 
        "comment": "nov | nov. | noviembre",
		"pattern": [
            {"LOWER": {"REGEX": r"^nov(?:\.|iembre)?$"}}            
        ]
    },
    { 
        # Dec
        "id": "http://vocab.getty.edu/aat/300410301",
        "label": "MONTHNAME", 
        "comment": "dic | dic. | diciembre",
		"pattern": [
            {"LOWER": {"REGEX": r"^dic(?:\.|iembre)?$"}}            
        ]
    }
]