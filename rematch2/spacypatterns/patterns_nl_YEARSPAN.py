"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_nl_YEARSPAN.py
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
patterns_nl_YEARSPAN = [
    { 
        "label": "YEARSPAN",
		"pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}}, 
            {"_": {"is_monthname": True}},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "*", "_": {"is_datesuffix": True}}
        ]
    },
    { 
        "label": "YEARSPAN", 
		"pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"_": {"is_seasonname": True}},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "*", "_": {"is_datesuffix": True}}
        ]
    },
    { 
        "label": "YEARSPAN",
		"pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"_": {"is_datesuffix": True}}
        ] 
    },
    { 
        "label": "YEARSPAN", 
		"pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"LOWER": {"REGEX": r"^\d+[\–\-/]\d+$"}},
            {"OP": "*", "_": {"is_datesuffix": True}}
        ] 
    },
    { 
        "label": "YEARSPAN", 
		"pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "*", "_": {"is_datesuffix": True}},
            {"_": {"is_dateseparator": True}}, 
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"_": {"is_datesuffix": True}}
        ] 
    },
    { 
        "label": "YEARSPAN", 
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
        "comment": "e.g. vijfde eeuw na Christus",
		"pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"_": {"is_ordinal": True}},
            {"LOWER": {"REGEX": r"^(eeuw|millennium)$"}},
            {"OP": "*", "_": {"is_datesuffix": True}}
        ]
    },
    { 
        "label": "YEARSPAN",         
        "comment": "e.g. vijfde eeuw na Christus",
		"pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"LOWER": {"REGEX": r"\d+e/\d+e"}},
            {"LOWER": {"REGEX": r"^(eeuw|millennium)$"}},
            {"OP": "*", "_": {"is_datesuffix": True}},
        ]
    },
    { 
        "label": "YEARSPAN",        
        "comment": "e.g. 14e - 15e eeuw",
		"pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"_": {"is_ordinal": True}},
            {"OP": "?", "LOWER": {"REGEX": r"^(eeuw|millennium)$"}},
            {"OP": "*", "_": {"is_datesuffix": True}},
            {"_": {"is_dateseparator": True}},
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"_": {"is_ordinal": True}},
            {"LOWER": {"REGEX": r"^(eeuw|millennium)$"}},
            {"OP": "*", "_": {"is_datesuffix": True}}
        ]
    }
]