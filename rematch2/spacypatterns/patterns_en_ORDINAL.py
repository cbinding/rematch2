patterns_en_ORDINAL = [
    { 
        "label": "ORDINAL",
		"pattern": [
           {"LOWER": {"IN": [
                "first","second","third","fourth","fifth",
                "sixth","seventh","eighth","ninth","tenth",
                "eleventh","twelfth","thirteenth","fourteenth","fifteenth",
                "sixteenth","seventeenth","eighteenth","nineteenth","twentieth" 
            ]}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^\d+(st|nd|rd|th)$"}}            
        ] 
    }
]