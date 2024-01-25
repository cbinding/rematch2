"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_cz_ORDINAL.py
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
patterns_cz_ORDINAL = [
    { 
        "label": "ORDINAL",
      	"pattern": [
            {"LOWER": {"IN": [
                "první", "druhý", "třetí", "čtvrtý", "pátý",
                "šestý", "sedmý", "osmý", "devátý", "desátý",
                "jedenáctý", "dvanáctý", "třináctý", "čtrnáctý", "patnáctý",
                "šestnáctý", "sedmnáctý", "osmnáctý", "devatenáctý", "dvacátý"
            ]}}
        ]
    }
]