"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_fr_YEARSPAN.py
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
siecle_millenaire = r"^s((\.|i[eè]cles?)?|mill[eé]naires?)$"

patterns_fr_YEARSPAN = [        
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
            {"OP": "+", "_": {"is_datesuffix": True}},
        ] 
    },
    { 
        "label": "YEARSPAN",
		"pattern": [
            {"ORTH": {"REGEX": r"^\d+[\–\-/]\d+$"}},
            {"OP": "*", "_": {"is_datesuffix": True}},
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
            {"OP": "*", "_": {"is_datesuffix": True}},
        ] 
    },
    { 
        "label": "YEARSPAN",
		"pattern": [ 
            {"OP": "?", "LOWER": {"REGEX": "^ann[eé]es?$"}},
            {"LOWER": {"REGEX": r"^\d+$"}}, 
            {"_": {"is_dateseparator": True}},
            {"LOWER": {"REGEX": r"^\d+$"}} 
        ]
    },    
    { 
        "label": "YEARSPAN",
		"pattern": [ 
            {"LOWER": {"REGEX": r"^(ann[eé]es?|en)$"}},
            {"LOWER": {"REGEX": r"^\d+$"}}
        ]
    },
    {
        "label": "YEARSPAN",
        "pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"_": {"is_ordinal": True}},
            {"LOWER": {"REGEX": siecle_millenaire}},
            {"OP": "*", "_": {"is_datesuffix": True}},
        ]
    },
    {
        "label": "YEARSPAN",
        "pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"_": {"is_ordinal": True}},
            {"OP": "?", "LOWER": {"REGEX": siecle_millenaire}},
            {"OP": "*", "_": {"is_datesuffix": True}},
            {"_": {"is_dateseparator": True}},
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"_": {"is_ordinal": True}},
            {"LOWER": {"REGEX": siecle_millenaire}},
            {"OP": "*", "_": {"is_datesuffix": True}},
        ]
    },
    {
        "label": "YEARSPAN",
        "pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"_": {"is_ordinal": True}},
            {"LOWER": {"REGEX": siecle_millenaire}},
            {"OP": "*", "_": {"is_datesuffix": True}},
            {"_": {"is_dateseparator": True}},
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"_": {"is_ordinal": True}},
            {"OP": "?", "LOWER": {"REGEX": siecle_millenaire}},
            {"OP": "*", "_": {"is_datesuffix": True}}
        ]
    }
]