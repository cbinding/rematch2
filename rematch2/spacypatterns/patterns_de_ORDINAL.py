"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_de_ORDINAL.py
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
patterns_de_ORDINAL = [
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(1\.|erste[sn]?)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(2\.|zweite[sn]?)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(3\.|dritte[sn]?)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(4\.|vierte[sn]?)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(5\.|fünfte[sn]?)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(6\.|sechste[sn]?)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(7\.|siebte[sn]?)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(8\.|achte[sn]?)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(9\.|neunte[sn]?)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(10\.|zehnte[sn]?)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(11\.|elfte[sn]?)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(12\.|zwölfte[sn]?)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(13\.|dreizehnte[sn]?)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(14\.|vierzehnte[sn]?)$"}} 
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(15\.|fünfzehnte[sn]?)$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(16\.|sechzehnte[sn]?)$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(17\.|siebzehnte[sn]?)$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(18\.|achtzehnte[sn]?)$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(19\.|neunzehnte[sn]?)$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(20\.|zwanzigste[sn]?)$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(21\.|einundzwanzigste[sn]?)$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(22\.|zweiundzwanzigste[sn]?)$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(23\.|dreiundzwanzigste[sn]?)$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(24\.|vierundzwanzigste[sn]?)$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(25\.|fünfundzwanzigste[sn]?)$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(26\.|sechsundzwanzigste[sn]?)$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(27\.|siebenundzwanzigste[sn]?)$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(28\.|achtundzwanzigste[sn]?)$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(29\.|neunundzwanzigste[sn]?)$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(30\.|dreißigste[sn]?)$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(31\.|einunddreißig)$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": "dreißig"},
            {"LOWER": "zuerst"}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": "einunddreißigsten"}
        ]
    }
]