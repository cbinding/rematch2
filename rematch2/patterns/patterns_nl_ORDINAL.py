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