"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_it_ORDINAL.py
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
patterns_it_ORDINAL = [
    { 
        "label": "ORDINAL",
		"pattern": [
           {"LOWER": {"IN": [
                "primo", "secondo", "terzo", "quarto", "quinto",
                "sesto", "settimo", "ottavo", "nono", "decimo",
                "undicesimo", "dodicesimo", "tredicesimo", "quattordicesimo", "quindicesimo",
                "sedicesimo", "diciassettesimo", "diciottesimo", "diciannovesimo", "ventesimo", 
                "ventunesimo", "ventiduesimo", "ventitreesimo", "ventiquattresimo", "venticinquesimo",
                "ventiseiesimo", "ventisettesimo", "ventotto", "ventinovesimo", "trentesimo", "trentunesimo"
            ]}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
           {"LOWER": {"IN": [
                "prima", "seconda", "terza", "quarta", "quinta",
                "sesta", "settima", "ottava", "nona", "decima",
                "undicesima", "dodicesima", "tredicesima", "quattordicesima", "quindicesima",
                "sedicesima", "diciassettesima", "diciottesima", "diciannovesima", "ventesima", 
                "ventunesima", "ventiduesima", "ventitreesima", "ventiquattresima", "venticinquesima",
                "ventiseiesima", "ventisettesima", "ventotta", "ventinovesima", "trentesima", "trentunesima"
            ]}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"TEXT": {"REGEX": r"^([MDCLXVI]+|\d+[°º])$"}}            
        ] 
    }
]