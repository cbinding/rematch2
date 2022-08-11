patterns_no_ORDINAL = [
    { 
        "label": "ORDINAL", 
        "language": "no",
        "pattern": [
            {"LOWER": {"IN": [
                "første", "annen", "anna", "annet", "andre", "tredje", "fjerde", 
                "femte", "sjette", "syvende", "sjuende", "åttende", "niende", "tiende",
                "ellevte", "tolvte", "trettende", "fjortende", "femtende", "sekstende",
                "syttende", "attende", "nittende", "tyvende", "tjuende", "tjueførste",
                "tjuesekund", "tjuetredje", "tjuefjerde", "tjuefemte", "tjuesjette",
                "tjuesyvende", "tjueåtte", "tjueniende", "tretti", "trettiførste"                  
            ]}}
        ]
    },
    { 
        "label": "ORDINAL", 
        "language": "no",
        "pattern": [
            {"LOWER": {"REGEX": r"^\d{1,2}$"}}            
        ] 
    }
]