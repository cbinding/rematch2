patterns_it_ORDINAL = [
    { 
        "label": "ORDINAL", 
        "language": "it",
        "pattern": [
           {"LOWER": {"IN": [
                "primo", "secondo", "terzo", "quarto", "quinto",
                "sesto", "settimo", "ottavo", "nono", "decimo",
                "undicesimo", "dodicesimo", "tredicesimo", "quattordicesimo", "quindicesimo",
                "sedicesimo", "diciassettesimo", "diciottesimo", "diciannovesimo", "ventesimo", 
                "ventunesimo", "ventiduesima", "ventitreesimo", "ventiquattresimo", "venticinquesimo",
                "ventiseiesimo", "ventisettesimo", "ventotto", "ventinovesimo", "trentesimo", "trentunesima"
            ]}}            
        ]
    },
    { 
        "label": "ORDINAL", 
        "language": "it",
        "pattern": [
            {"TEXT": {"REGEX": r"^([MDCLXVI]+|\d+[°º])$"}}            
        ] 
    }
]