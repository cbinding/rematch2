"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_de_DATESUFFIX.py
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
patterns_de_DATESUFFIX = [
  {
    "id": "ad1",
    "label": "DATESUFFIX",
    "pattern": [{"LOWER": {"REGEX": r"^a\.?d\.?$"}}]
  },  
  {
    "id": "bc",
    "label": "DATESUFFIX",
    "pattern": [{"LOWER": {"REGEX": r"^b\.?c\.?$"}}]
  }, 
  {
    "id": "ad2",
    "label": "DATESUFFIX",
    "pattern": [{"LOWER": {"REGEX": r"^c\.?e\.?$"}}]
  },   
  {
    "id": "bce",
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
    "id": "ad3",
    "label": "DATESUFFIX",
    "pattern": [
        {"LOWER": {"REGEX": r"^n\.?$"}},
        {"LOWER": {"REGEX": r"^chr\.?$"}}
      ]
  }, 
  {
    "id": "ad4",
    "label": "DATESUFFIX",
    "pattern": [
        {"LOWER": "na"}, 
        {"LOWER": "christus"}
      ]
  },   
  {
    "id": "ad5",
    "label": "DATESUFFIX",
    "pattern": [
        {"LOWER": {"REGEX": r"^v\.?$"}},
        {"LOWER": {"REGEX": r"^chr\.?$"}}
      ]
  },    
  {
    "id": "ad6",
    "label": "DATESUFFIX",
    "pattern": [
        {"LOWER": "vor"}, 
        {"LOWER": "christus"}
      ]
  }  
]