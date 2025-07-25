"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_no_YEARSPAN.py
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
patterns_no_YEARSPAN = [
    {
        "label": "YEARSPAN",
        "pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ENT_TYPE": "MONTHNAME"},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ]
    },
    {
        "label": "YEARSPAN",
        "pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ENT_TYPE": "SEASONNAME"},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ]
    },
    {
        "label": "YEARSPAN",
        "pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"},
            {"ENT_TYPE": "DATESEPARATOR"},
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"},
        ]
    },
    {
        "label": "YEARSPAN",
        "pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ORTH": {"REGEX": r"^\d+[\–\-/]\d+$"}},
            {"ENT_TYPE": "DATESUFFIX"},
        ]
    },
    {
        "label": "YEARSPAN",
        "pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"ORTH": {"REGEX": r"^\\p{pD}$"}},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"ENT_TYPE": "DATESUFFIX"},
        ]
    },
    {
        "label": "YEARSPAN",
        "pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ORTH": {"REGEX": r"^\d+±\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"},
            {"ENT_TYPE": "DATESEPARATOR"},
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ORTH": {"REGEX": r"^\d+±\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ]
    },
    {
        "label": "YEARSPAN",
        "pattern": [
            {"LOWER": {"REGEX": r"^\d+±\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ]
    },
    {
        "label": "YEARSPAN",
        "pattern": [
            {"LOWER": {"REGEX": r"^\d+$"}},
            {"LOWER": {"REGEX": r"^(bp)?±\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ]
    },
    {
        "label": "YEARSPAN",
        "pattern": [
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "+", "ENT_TYPE": "DATESUFFIX"}
        ]
    },
    { 
        "label": "YEARSPAN",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"LOWER": {"REGEX": r"^\d+00\-tallets?$"}},            
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ]
    },
    { 
        "label": "YEARSPAN",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ENT_TYPE": "ORDINAL"},
            {"LOWER": {"REGEX": r"^(århundre|årtusen)$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ]
    },
    { 
        "label": "YEARSPAN",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ENT_TYPE": "ORDINAL"},
            {"OP": "?", "LOWER": {"REGEX": r"^(?:århundre|årtusen)$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"},
            {"ENT_TYPE": "DATESEPARATOR"},
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ENT_TYPE": "ORDINAL"},
            {"LOWER": {"REGEX": r"^(?:århundre|årtusen)$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ]
    }
]
