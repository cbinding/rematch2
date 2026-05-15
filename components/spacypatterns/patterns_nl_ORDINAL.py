"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_nl_ORDINAL.py
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
patterns_nl_ORDINAL = [
    { 
        "label": "ORDINAL",
		"pattern": [
           {"LOWER": {"IN": [
                "eerste", "tweede", "derde", "vierde", "vijfe",
                "zesde", "zevende", "achtse", "negende", "tiende",
                "elfde", "twaalfde", "dertiende", "veertiende", "vijftiende",
                "zestiende", "zeventiende", "achttiende", "negentiende", "twintigste",
                "eenentwintigste", "tweeëntwintigste", "drieëntwintig", "vierentwintig", 
                "vijfentwintig", "zesentwintig", "zevenentwintig", "achtentwintig", 
                "negenentwintig", "dertigste", "eenendertigste" 
            ]}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^\d+e$"}}            
        ] 
    }
]