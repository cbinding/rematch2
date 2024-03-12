"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_en_YEARSPAN.py
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
patterns_en_YEARSPAN = [
    {
        "label": "YEARSPAN",
        "comment": "e.g. start of March 1715 AD",
        "pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ENT_TYPE": "MONTHNAME"},
            {"ORTH": {"REGEX": r"^\d{4}$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ]
    },
    {
        "label": "YEARSPAN",
        "comment": "e.g. mid autumn 1715 AD",
        "pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ENT_TYPE": "SEASONNAME"},
            {"ORTH": {"REGEX": r"^\d{4}$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ]
    },
    {
        "label": "YEARSPAN",
        "comment": "year with tolerance e.g. 1715±9 AD",
        "pattern": [
            {"ORTH": {"REGEX": r"^\d+±\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ]
    },
    {
        "label": "YEARSPAN",
        "comment": "year with tolerance e.g. 1715+9-5 AD",
        "pattern": [
            {"ORTH": {"REGEX": r"^\d+\+\d+\-\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ]
    },
    {
        "label": "YEARSPAN",
        "comment": "e.g. mid 1580 AD",
        "pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ORTH": {"REGEX": r"^\d{3,4}$"}},
            {"OP": "+", "ENT_TYPE": "DATESUFFIX"}
        ]
    },
    {
        "label": "YEARSPAN",
        "comment": "e.g. 1580 to 1690 AD",
        "pattern": [
            {"ORTH": {"REGEX": r"^\d{3,4}$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"},
            {"ENT_TYPE": "DATESEPARATOR"},
            {"ORTH": {"REGEX": r"^\d{3,4}$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ]
    },
    {
        "label": "YEARSPAN",
        "comment": "e.g. early 100 BC to late 100 AD",
        "pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ORTH": {"REGEX": r"^\d{3,4}$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"},
            {"ENT_TYPE": "DATESEPARATOR"},
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ORTH": {"REGEX": r"^\d{3,4}}$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ]
    },
    { 
        "label": "YEARSPAN",         
        "comment": "e.g. beginning of the fifth century AD",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "ORDINAL"},
            {"LOWER": {"REGEX": r"^(century|centuries|millennium|millennia)$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"} 
        ]
    },
    { 
        "label": "YEARSPAN",         
        "comment": "e.g. start of the first to end of the 2nd century AD",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "ORDINAL"},
            {"OP": "?", "LOWER": {"REGEX": r"^(century|centuries|millennium|millennia)$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"},
            {"ENT_TYPE": "DATESEPARATOR"},
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"ENT_TYPE": "ORDINAL"},
            {"LOWER": {"REGEX": r"^(century|centuries|millennium|millennia)$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"} 
        ]
    }
]
