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
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"_": {"is_monthname": True}},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "*", "_": {"is_datesuffix": True}}
        ]
    },
    { 
        "label": "YEARSPAN",         
        "comment": "",
		"pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}}, 
            {"_": {"is_seasonname": True}},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "*", "_": {"is_datesuffix": True}}
        ]
    },
    { 
        "label": "YEARSPAN",         
        "comment": "",
		"pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "+", "_": {"is_datesuffix": True}}
        ] 
    },
    { 
        "label": "YEARSPAN",        
        "comment": "",
		"pattern": [
            {"ORTH": {"REGEX": r"^\d+(?:[/\–\-a]|all[a'])\d+$"}},
            {"OP": "*", "_": {"is_datesuffix": True}}
        ] 
    },
    { 
        "label": "YEARSPAN",         
        "comment": "",
		"pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}}, 
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "*", "_": {"is_datesuffix": True}}, 
            {"_": {"is_dateseparator": True}},
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "*", "_": {"is_datesuffix": True}}
        ] 
    },
    { 
        "label": "YEARSPAN",
		"pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}}, 
            {"_": {"is_ordinal": True}}, 
            {"LOWER": {"REGEX": r"^(sec(olo|\.)|mill(ennio|\.))$"}},
            {"OP": "*", "_": {"is_datesuffix": True}}, 
        ]
    },
    { 
        "label": "YEARSPAN",
		"pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}},  
            {"TEXT": {"REGEX": r"[MCDLXVI]+"}}, 
            {"LOWER": {"REGEX": r"^(sec(olo|\.)|mill(ennio|\.))$"}},
            {"OP": "*", "_": {"is_datesuffix": True}}, 
        ]
    },
    { 
        "label": "YEARSPAN",
		"pattern": [
            {"TEXT": {"REGEX": r"[MCDLXVI]+\-[MCDLXVI]+"}}, 
            {"LOWER": {"REGEX": r"^(sec(olo|\.)|mill(ennio|\.))$"}},
            {"OP": "*", "_": {"is_datesuffix": True}}, 
        ]
    },
    { 
        "label": "YEARSPAN",
		"pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}}, 
            {"_": {"is_ordinal": True}}, 
            {"OP": "?", "LOWER": {"REGEX": r"^(sec(olo|\.)|mill(ennio|\.))$"}},
            {"OP": "*", "_": {"is_datesuffix": True}}, 
            {"_": {"is_dateseparator": True}}, 
            {"OP": "*", "_": {"is_dateprefix": True}}, 
            {"_": {"is_ordinal": True}},
            {"LOWER": {"REGEX": r"^(sec(olo|\.)|mill(ennio|\.))$"}},
            {"OP": "*", "_": {"is_datesuffix": True}}
        ]
    },
    { 
        "label": "YEARSPAN",
		"pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"_": {"is_ordinal": True}},
            {"LOWER": {"REGEX": r"^(sec(olo|\.)|mill(ennio|\.))$"}},
            {"OP": "*", "_": {"is_datesuffix": True}},
            {"_": {"is_dateseparator": True}},
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"_": {"is_ordinal": True}},
            {"OP": "?", "LOWER": {"REGEX": r"^(sec(olo|\.)|mill(ennio|\.))$"}},
            {"OP": "*", "_": {"is_datesuffix": True}}
        ]
    }
]