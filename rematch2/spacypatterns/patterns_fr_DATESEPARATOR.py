"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_fr_DATESEPARATOR.py
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
patterns_fr_DATESEPARATOR = [
    {
        "label": "DATESEPARATOR",
        "pattern": [
            {"LOWER": {"REGEX": r"^(?:[\–\-/]|au|et|à)$"}}
        ]
    }
]
