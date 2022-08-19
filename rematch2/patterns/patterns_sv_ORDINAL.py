patterns_sv_ORDINAL = [
    { 
        "label": "ORDINAL",
		"pattern": [
           {"LOWER": {"IN": [
                "första", "andra", "tredje", "fjärde", "femte",
                "sjätte", "sjunde", "åttonde", "nionde", "tionde",
                "elfte", "tolfte", "trettonde", "fjortonde", "femtonde",
                "sextonde", "sjuttonde", "artonde", "nittonde", "tjugonde",
                "tjugoförsta","tjugoandra","tjugotredje","tjugofjärde","tjugofemte",
                "tjugosjätte", "tjugosjunde", "tjugoåttonde", "tjugonionde", 
                "trettionde", "trettioförsta"
            ]}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^\d+[ae]$"}}            
        ] 
    }
]