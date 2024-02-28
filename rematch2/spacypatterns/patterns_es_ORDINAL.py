"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_es_ORDINAL.py
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
patterns_es_ORDINAL = [
    { 
        "label": "ORDINAL",
		"pattern": [
            {"TEXT": {"REGEX": r"^([MDCLXVI]+|\d+[°º])$"}}            
        ] 
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(1°|i|primer[oa]?)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(2°|ii|2do|segund[oa])$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(3°|iii|3ro|tercer[oa]?)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(4°|iv|4to|cuart[oa])$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(5°|v|5to|quint[oa])$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(6°|vi|6to|sext[oa])$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(7°|vii|7mo|séptim[oa])$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(8°|viii|8vo|octav[oa])$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(9°|ix|9no|noven[oa])$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(10°|x|10mo|décim[oa])$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(11°|xi|11mo|undécim[oa])$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(12°|xii|12mo|duodécim[oa])$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(13°|xiii|13ro|decimotercer[oa])$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(14°|xiv|14to|decimocuart[oa])$"}} 
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(15°|xv|15to|decimoquint[oa])$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(16°|xvi|16to|decimosext[oa])$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(17°|xvii|17mo|decimoséptim[oa])$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(18°|xviii|18vo|decimoctav[oa])$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(19°|xix|19no|decimonoven[oa])$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(20°|xx|20mo|vigésim[oa])$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(21°|xxi|21ro|vigésimoprimer[oa])$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(22°|xxii|22do|vigésimosegund[oa])$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(23°|xxiii|23ro|vigésimotercer[oa])$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(24°|xxiv|24to|vigésimocuart[oa])$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(25°|xxv|25to|vigésimoquint[oa])$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(26°|xxvi|26to|vigésimosext[oa])$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(27°|xxvii|27mo|vigésimoséptim[oa])$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(28°|xxviii|28vo|vigésimooctav[oa])$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(29°|xxix|29no|vigésimonoven[oa])$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(30°|xxx|30mo|trigésim[oa])$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(31°|xxxi|31ro|trigésimoprimer[oa])$"}}
        ]
    }
]