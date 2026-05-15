"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_en_YEARSPAN.py
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
patterns_en_YEARSPAN = [
    {
        "label": "YEARSPAN",
        "comment": "Month and year e.g. start of March 1715 AD",
        "pattern": [
            #{"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ENT_TYPE": "MONTHNAME"},
            {"ORTH": {"REGEX": r"^\d{4}$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ]
    },
    { 
        "label": "YEARSPAN",        
        "comment": "e.g. June to September 1715 AD",
		"pattern": [
            #{"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ENT_TYPE": "MONTHNAME"},
            {"ENT_TYPE": "DATESEPARATOR"},
            #{"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ENT_TYPE": "MONTHNAME"},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ]
    },
    {
        "label": "YEARSPAN",
        "comment": "Season and year e.g. mid autumn 1715 AD",
        "pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ENT_TYPE": "SEASONNAME"},
            {"ORTH": {"REGEX": r"^\d{4}$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ]
    },
    {
        "label": "YEARSPAN",
        "comment": "Season and year e.g. mid spring to autumn 1715 AD",
        "pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ENT_TYPE": "SEASONNAME"},
            {"OP": "?", "ENT_TYPE": "DATESEPARATOR"},
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ENT_TYPE": "SEASONNAME"},
            {"ORTH": {"REGEX": r"^\d{4}$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ]
    },
    {
        "label": "YEARSPAN",
        "comment": "decade e.g. late 1920s",
        "pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ORTH": {"REGEX": r"^\d{4}s$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ]
    },
    {
        "label": "YEARSPAN",
        "comment": "year with tolerance e.g. 1715±9 AD",
        "pattern": [
            {"ORTH": {"REGEX": r"^\d+±\d+$"}},
            {"OP": "+", "ENT_TYPE": "DATESUFFIX"}
        ]
    },
    {
        "label": "YEARSPAN",
        "comment": "year with tolerance e.g. 1715+9-5 AD",
        "pattern": [
            {"ORTH": {"REGEX": r"^\d+\+\d+\-\d+$"}},
            {"OP": "+", "ENT_TYPE": "DATESUFFIX"}
        ]
    },
    {
        "label": "YEARSPAN",
        "comment": "e.g. 2.3 ka BP",
        "pattern": [
            {"LIKE_NUM": True},
            {"LOWER":"ka"},
            {"ENT_TYPE": "DATESUFFIX"}
        ]
    },
    {
        "label": "YEARSPAN",
        "comment": "year with prefix e.g. early 1580 AD",
        "pattern": [
            {"OP": "+", "ENT_TYPE": "DATEPREFIX"},
            {"ORTH": {"REGEX": r"^\d{3,4}$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ]
    },
    {
        "label": "YEARSPAN",
        "comment": "year with suffix e.g. 1580 AD",
        "pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ORTH": {"REGEX": r"^\d{3,4}$"}},
            {"OP": "+", "ENT_TYPE": "DATESUFFIX"}
        ]
    }, 
    {
        "label": "YEARSPAN",
        "comment": "year with prefix to year with prefix e.g. circa 1580 to circa 1600, maybe suffixes",
        "pattern": [
            {"OP": "+", "ENT_TYPE": "DATEPREFIX"},
            {"ORTH": {"REGEX": r"^\d{3,4}$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"},
            {"OP": "+", "ENT_TYPE": "DATESEPARATOR"},
            {"OP": "+", "ENT_TYPE": "DATEPREFIX"},
            {"ORTH": {"REGEX": r"^\d{3,4}$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"},
        ]
    },   
    {
        "label": "YEARSPAN",
        "comment": "year with suffix to year with suffix e.g. 1580 AD to 1600 AD, maybe prefixes",
        "pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ORTH": {"REGEX": r"^\d{3,4}$"}},
            {"OP": "+", "ENT_TYPE": "DATESUFFIX"},
            {"OP": "+", "ENT_TYPE": "DATESEPARATOR"},
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ORTH": {"REGEX": r"^\d{3,4}$"}},
            {"OP": "+", "ENT_TYPE": "DATESUFFIX"},
        ]
    },   
    {
        "label": "YEARSPAN",
        "comment": "year to year with suffix e.g. 1580 to 1600 AD, maybe prefixes",
        "pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ORTH": {"REGEX": r"^\d{3,4}$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"},
            {"OP": "+", "ENT_TYPE": "DATESEPARATOR"},
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ORTH": {"REGEX": r"^\d{3,4}$"}},
            {"OP": "+", "ENT_TYPE": "DATESUFFIX"},
        ]
    },   
    #{
    #    "label": "YEARSPAN",
    #    "comment": "year span e.g. early 100 BC to late 100 AD",
    #    "pattern": [
    #        {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
    #        {"ORTH": {"REGEX": r"^\d{3,4}$"}},            
    #        {"OP": "*", "ENT_TYPE": "DATESUFFIX"},
    #        {"OP": "+", "ENT_TYPE": "DATESEPARATOR"},
    #        {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
    #        {"ORTH": {"REGEX": r"^\d{3,4}$"}},
    #        {"OP": "*", "ENT_TYPE": "DATESUFFIX"},
    #    ]
    #},    
    { 
        "label": "YEARSPAN",         
        "comment": "ordinal century e.g. beginning of the fifth century AD",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"OP": "?", "ORTH": "-"},
            {"ENT_TYPE": "ORDINAL"},
            {"OP": "?", "ORTH": "-"},
            {"LOWER": {"REGEX": r"^(century|centuries|millennium|millennia)$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"},
        ]
    },
    #{
        #"label": "YEARSPAN",
        #"comment": "shorthand century e.g. C19",
        #"pattern": [
           # {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            #{"ORTH": {"REGEX": r"^C[12]\d$"}},            
            #{"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        #]
    #},
    {
        "label": "YEARSPAN",
        "comment": "shorthand century span e.g. C19 - C20",
        "pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            #{"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ORTH": {"REGEX": r"^C[12]\d$"}},
            {"ENT_TYPE": "DATESEPARATOR"},
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            #{"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"ORTH": {"REGEX": r"^C[12]\d$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ]
    },
    { 
        "label": "YEARSPAN",         
        "comment": "ordinal century span e.g. start of the first to end of the 2nd century AD",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"OP": "?", "ORTH": "-"},
            {"OP": "+", "ENT_TYPE": "ORDINAL"},
            {"OP": "?", "LOWER": {"REGEX": r"^(century|centuries|millennium|millennia)$"}},            
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"},
            {"OP": "+", "ENT_TYPE": "DATESEPARATOR"},
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"OP": "?", "ORTH": "-"},
            {"OP": "+", "ENT_TYPE": "ORDINAL"},
            {"LOWER": {"REGEX": r"^(century|centuries|millennium|millennia)$"}},
            {"OP": "*", "ENT_TYPE": "DATESUFFIX"}
        ]
    }
]
