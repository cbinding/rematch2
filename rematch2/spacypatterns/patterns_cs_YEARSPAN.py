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
stoleti_tisicileti = r"^(?:stol(?:\.|etí)?|tisícil(?:\.|etí)?)$"

patterns_cs_YEARSPAN = [
    {
        "label": "YEARSPAN",
        "comment": "Month and year e.g. start of March 1715 AD",
        "pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"_": {"is_monthname": True}},
            {"ORTH": {"REGEX": r"^\d{4}$"}},
            {"OP": "*", "_": {"is_datesuffix": True}}
        ]
    },
    {
        "label": "YEARSPAN",
        "comment": "Season and year e.g. mid autumn 1715 AD",
        "pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"_": {"is_seasonname": True}},
            {"ORTH": {"REGEX": r"^\d{4}$"}},
            {"OP": "*", "_": {"is_datesuffix": True}}
        ]
    },
    {
        "label": "YEARSPAN",
        "comment": "decade e.g. late 1920s",
        "pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"ORTH": {"REGEX": r"^\d{4}s$"}},
            {"OP": "+", "_": {"is_datesuffix": True}}
        ]
    },
    {
        "label": "YEARSPAN",
        "comment": "year with tolerance e.g. 1715±9 AD",
        "pattern": [
            {"ORTH": {"REGEX": r"^\d+±\d+$"}},
            {"OP": "+", "_": {"is_datesuffix": True}}
        ]
    },
    {
        "label": "YEARSPAN",
        "comment": "year with tolerance e.g. 1715+9-5 AD",
        "pattern": [
            {"ORTH": {"REGEX": r"^\d+\+\d+\-\d+$"}},
            {"OP": "+", "_": {"is_datesuffix": True}}
        ]
    },
    {
        "label": "YEARSPAN",
        "comment": "year with prefix e.g. early 1580 AD",
        "pattern": [
            {"OP": "+", "_": {"is_dateprefix": True}},
            {"ORTH": {"REGEX": r"^\d{3,4}$"}},
            {"OP": "*", "_": {"is_datesuffix": True}}
        ]
    },
    {
        "label": "YEARSPAN",
        "comment": "year with suffix e.g. 1580 AD",
        "pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"ORTH": {"REGEX": r"^\d{3,4}$"}},
            {"OP": "+", "_": {"is_datesuffix": True}}
        ]
    },    
    {
        "label": "YEARSPAN",
        "comment": "year span e.g. early 100 BC to late 100 AD",
        "pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"ORTH": {"REGEX": r"^\d{3,4}$"}},            
            {"OP": "*", "_": {"is_datesuffix": True}},
            {"_": {"is_dateseparator": True}},
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"ORTH": {"REGEX": r"^\d{3,4}}$"}},
            {"OP": "*", "_": {"is_datesuffix": True}},
        ]
    },
    { 
        "label": "YEARSPAN",
        "id": "ordinalcentury",
		"pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}}, 
            {"OP": "+", "_": {"is_ordinal": True}},
            {"LOWER": {"REGEX": stoleti_tisicileti}},
            {"OP": "?","TEXT": "."},
            {"OP": "*", "_": {"is_datesuffix": True}},
        ]
    },
    { 
        "label": "YEARSPAN",
		"pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}}, 
            {"OP": "+", "_": {"is_ordinal": True}},
            {"OP": "?", "LOWER": {"REGEX": stoleti_tisicileti}},
            {"OP": "?","TEXT": "."},
            {"OP": "*", "_": {"is_datesuffix": True}},
            {"_": {"is_dateseparator": True}},
            {"OP": "*", "_": {"is_dateprefix": True}}, 
            {"OP": "+", "_": {"is_ordinal": True}},
            {"LOWER": {"REGEX": stoleti_tisicileti}},
            {"OP": "?","TEXT": "."},
            {"OP": "*", "_": {"is_datesuffix": True}}
        ]
    }
]