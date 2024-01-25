"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_fr_ORDINAL.py
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
patterns_fr_ORDINAL = [
    { 
        "label": "ORDINAL",
		"pattern": [
            { "LOWER": { "IN": [
                "premier", "deuxième", "second", "troisième", "quatrième", "cinquième",
                "sixième", "septième", "huitième", "neuvième", "dixième", "onzième",
                "douzième", "treizième", "quatorzième", "quinzième", "seizième",
                "dix-septième", "dix-huitième", "dix-neuvième", "vingtième" 
            ]}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            # using negative lookahead to restrict to POS != 'DET'. Any better way??
            # otherwise 'Le' and 'De' would be inappropriately matched as ordinals.. 
            {"POS": {"REGEX": r"^(?!DET)\w{3,}$"}, "TEXT": {"REGEX": r"^([MDCLXVI]+|\d+)(er?|[eè]me)$"}}
            #{"TEXT": {"REGEX": r"^([MDCLXVI]+|\d+)(er?|[eè]me)$"}}               
        ] 
    }
]
