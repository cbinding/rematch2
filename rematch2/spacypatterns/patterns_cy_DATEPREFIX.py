"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_cy_DATEPREFIX.py
Version :   20221027
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   ARIADNEplus
Summary :   spaCy patterns for use with pipeline            
Imports :   
Example :           
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
History :   27/10/2022 CFB Initially created script
=============================================================================
"""
patterns_cy_DATEPREFIX = [
    {
        "label": "DATEPREFIX",
        "pattern": [
            {"LOWER": {"REGEX": r"^(ca?\.?|circa|oddeuta|tua\'r)$"}}
        ]
    },
    {
        "label": "DATEPREFIX",
        "pattern": [
            {"LOWER": "o"},
            {"LOWER": "gwmpas"}
        ]
    },
    {
        "label": "DATEPREFIX",
        "pattern": [
            {"LOWER": "hanner"},
            {"LOWER": "cyntaf"},
            {"OP": "?", "LOWER": "y"}
        ]
    },
    {
        "label": "DATEPREFIX",
        "pattern": [
            {"LOWER": "canol"},
            {"OP": "?", "LOWER": "y"}
        ]
    }
]
