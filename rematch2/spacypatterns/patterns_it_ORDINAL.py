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