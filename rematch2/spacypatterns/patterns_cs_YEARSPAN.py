"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_cs_YEARSPAN.py
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
patterns_cs_YEARSPAN = [    
    { 
        "label": "YEARSPAN",         
        "comment": "e.g. 'start of March 1715 AD', or 'mid autumn 1715 AD'",
		"pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"_": {"is_seasonname": True}},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "*", "_": {"is_datesuffix": True}}
        ]
    },    
    { 
        "label": "YEARSPAN",        
        "comment": "e.g. mid 1580 AD",
		"pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "+", "_": {"is_datesuffix": True}}
        ] 
    },
    { 
        "label": "YEARSPAN",         
        "comment": "e.g. 1400 - 1500 AD",
		"pattern": [
            {"ORTH": {"REGEX": r"^\d+[\–\-]\d+$"}},
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
            {"OP": "?", "LOWER": {"REGEX": r"^(?:století|tisícil(?:\.|etí))$"}},
            {"OP": "*", "_": {"is_datesuffix": True}},
            {"_": {"is_dateseparator": True}},
            {"OP": "*", "_": {"is_dateprefix": True}}, 
            {"_": {"is_ordinal": True}},
            {"LOWER": {"REGEX": r"^(?:století|tisícil(?:\.|etí))$"}},
            {"OP": "*", "_": {"is_datesuffix": True}}
        ]
    },
    { 
        "label": "YEARSPAN",
		"pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}}, 
            {"_": {"is_ordinal": True}},
            {"LOWER": {"REGEX": r"^(?:století|tisícil(?:\.|etí))$"}},
            {"OP": "*", "_": {"is_datesuffix": True}},
        ]
    }
]