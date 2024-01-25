"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_fr_DATESUFFIX.py
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
avant_apres = r"^(av(\.|ant)?|ap(\.|r\.?|r[eè]s)?|de)$"

patterns_fr_DATESUFFIX = [
    {
        "label": "DATESUFFIX",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": r"cal\.?"}},
            {"LOWER": {"REGEX": r"^(ad|bc|bp|a\.d\.|b\.c\.|b\.p\.)$"}}
        ]
    },
    {
        "label": "DATESUFFIX",
        "pattern": [
            {"LOWER": {"REGEX": avant_apres}},
            {"LOWER":  {"REGEX": r"^j\.?$"}},
            {"LOWER":  {"REGEX": r"^\-?c\.?$"}}
        ]
    },
    {
        "label": "DATESUFFIX",
        "pattern": [
            {"LOWER": {"REGEX": avant_apres}},
            {"LOWER":  "jc"}
        ]
    },
    {
        "label": "DATESUFFIX",
        "pattern": [
            {"LOWER": {"REGEX": avant_apres}},
            {"LOWER":  {"REGEX": r"^j\.-c\.?$"}}
        ]
    },
    {
        "label": "DATESUFFIX",
        "pattern": [
            {"LOWER": {"REGEX": avant_apres}},
            {"LOWER":  {"REGEX": r"^j\.?$"}},
            {"OP": "?", "TEXT":  "-"},
            {"LOWER":  {"REGEX": r"^c\.?$"}}
        ]
    },
    {
        "label": "DATESUFFIX",
        "pattern": [
            {"LOWER": {"REGEX": avant_apres}},
            {"LOWER": {"REGEX": r"^n(\.|otre)$"}},
            {"LOWER":  {"REGEX": r"^[eè]re$"}}
        ]
    },
    {
        "label": "DATESUFFIX",
        "pattern": [
            {"LOWER": {"REGEX": avant_apres}},
            {"LOWER": {"REGEX": r"^n\.[eè]$"}}
        ]
    },
    {
        "label": "DATESUFFIX",
        "pattern": [
            {"LOWER": {"REGEX": avant_apres}},
            {"LOWER": {"REGEX": r"^n\.$"}},
            {"LOWER": {"REGEX": "^è$"}}
        ]
    }
]
