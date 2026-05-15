"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_cs_DATESUFFIX.py
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
patterns_cs_DATESUFFIX = [
  {
    "id": "ad",
    "label": "DATESUFFIX",
    "pattern": "AD"
  }, 
  {
    "id": "ad",
    "label": "DATESUFFIX",
    "pattern": "A.D."
  }, 
  {
    "id": "ad",
    "label": "DATESUFFIX",
    "pattern": "našeho letopočtu"
  },  
  {
    "id": "ad",
    "label": "DATESUFFIX",
    "pattern": "n. l."
  }, 
  {
    "id": "ce",
    "label": "DATESUFFIX",
    "pattern": "CE"
  }, 
  {
    "id": "ce",
    "label": "DATESUFFIX",
    "pattern": "C.E."
  }, 
  {
    "id": "bc",
    "label": "DATESUFFIX",
    "pattern": "BC"
  },
  {
    "id": "bc",
    "label": "DATESUFFIX",
    "pattern": "B.C."
  },   
  {
    "id": "bc",
    "label": "DATESUFFIX",
    "pattern": "př. n. l."
  }, 
  {
    "id": "bce",
    "label": "DATESUFFIX",
    "pattern": "BCE"
  },
  {
    "id": "bce",
    "label": "DATESUFFIX",
    "pattern": "B.C.E."
  },
  {
    "id": "bp",
    "label": "DATESUFFIX",
    "pattern": "BP"
  },
  {
    "id": "bp",
    "label": "DATESUFFIX",
    "pattern": "B.P."
  },
  {
    "id": "bp",
    "label": "DATESUFFIX",
    "pattern": "cal. BP"
  },
  {
    "id": "bp",
    "label": "DATESUFFIX",
    "pattern": "cal. B.P."
  },
]