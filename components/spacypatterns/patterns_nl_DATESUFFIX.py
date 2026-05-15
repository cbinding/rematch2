"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_nl_DATESUFFIX.py
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
patterns_nl_DATESUFFIX = [
    {
    "id": "ad",
    "label": "DATESUFFIX",
    "pattern": [{"LOWER": {"REGEX": r"^a\.?d\.?$"}}]
  },  
  {
    "id": "bc",
    "label": "DATESUFFIX",
    "pattern": [{"LOWER": {"REGEX": r"^b\.?c\.?$"}}]
  }, 
  {
    "id": "ad",
    "label": "DATESUFFIX",
    "pattern": [{"LOWER": {"REGEX": r"^c\.?e\.?$"}}]
  },   
  {
    "id": "bc",
    "label": "DATESUFFIX",
    "pattern": [{"LOWER": {"REGEX": r"^b\.?c\.?e\.?$"}}]
  },
  {
    "id": "bp",
    "label": "DATESUFFIX",
    "pattern": [
      {"OP": "*", "LOWER": {"REGEX": r"^cal\.?$"}},
      {"LOWER": {"REGEX": r"^b\.?p\.?$"}}
    ]
  },
    { 
        "label": "DATESUFFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(na?\.?|voor|vóór|v\.?)$"}},
            {"LOWER": {"REGEX": r"^(christus|chr\.?)$"}}
        ]
    },
    { 
        "label": "DATESUFFIX",
		"pattern": [
            {"OP": "?", "LOWER": "år"},
            {"LOWER": "före"},
            {"LOWER": "nutid"}
        ]
    }
]