"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_no_ORDINAL.py
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
patterns_no_ORDINAL = [
    { 
        "label": "ORDINAL",
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
		"pattern": [
            {"LOWER": {"REGEX": r"^\d+\.$"}}            
        ] 
    }
]