"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_it_YEARSPAN.py
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
patterns_it_YEARSPAN = [
    { 
        "label": "YEARSPAN", 
        "comment": "",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ENT_TYPE": "MONTHNAME"},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ]
    },
    { 
        "label": "YEARSPAN",         
        "comment": "",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "SEASONNAME"},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ]
    },
    { 
        "label": "YEARSPAN",         
        "comment": "",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "+", "ENT_TYPE": "DATESUFFIX"}
        ] 
    },
    { 
        "label": "YEARSPAN",        
        "comment": "",
		"pattern": [
            {"ORTH": {"REGEX": r"^\d+(?:[/\–\-a]|all[a'])\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ] 
    },
    { 
        "label": "YEARSPAN",         
        "comment": "",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}, 
            {"ENT_TYPE": "DATESEPARATOR"},
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ] 
    },
    { 
        "label": "YEARSPAN",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "ORDINAL"}, 
            {"LOWER": {"REGEX": r"^(sec(olo|\.)|mill(ennio|\.))$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}, 
        ]
    },
    { 
        "label": "YEARSPAN",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},  
            {"TEXT": {"REGEX": r"[MCDLXVI]+"}}, 
            {"LOWER": {"REGEX": r"^(sec(olo|\.)|mill(ennio|\.))$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}, 
        ]
    },
    { 
        "label": "YEARSPAN",
		"pattern": [
            {"TEXT": {"REGEX": r"[MCDLXVI]+\-[MCDLXVI]+"}}, 
            {"LOWER": {"REGEX": r"^(sec(olo|\.)|mill(ennio|\.))$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}, 
        ]
    },
    { 
        "label": "YEARSPAN",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "ORDINAL"}, 
            {"OP": "?", "LOWER": {"REGEX": r"^(sec(olo|\.)|mill(ennio|\.))$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}, 
            {"ENT_TYPE": "DATESEPARATOR"}, 
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "ORDINAL"},
            {"LOWER": {"REGEX": r"^(sec(olo|\.)|mill(ennio|\.))$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ]
    },
    { 
        "label": "YEARSPAN",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ENT_TYPE": "ORDINAL"},
            {"LOWER": {"REGEX": r"^(sec(olo|\.)|mill(ennio|\.))$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"},
            {"ENT_TYPE": "DATESEPARATOR"},
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ENT_TYPE": "ORDINAL"},
            {"OP": "?", "LOWER": {"REGEX": r"^(sec(olo|\.)|mill(ennio|\.))$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ]
    }
]