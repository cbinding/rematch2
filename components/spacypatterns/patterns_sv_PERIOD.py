"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_sv_PERIOD.py
Version :   20240125
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy patterns for use with SpanRuler pipeline components            
Imports :   
Example :           
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
History :   25/01/2024 CFB Initially created script
=============================================================================
"""
patterns_sv_PERIOD = [ 
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": "paleolitikum"}
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": "förhistorisk"},
            {"LOWER": "tid"}
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"OP": "?", "LOWER": {"REGEX": r"^(?:äldre|yngre)$"}},
            {"LOWER": {"REGEX": r"^stenåldern?"}}
                     
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^(?:tidig|mellan|sen)mesolitikum$"}}
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^(?:magle|konge)mosekulturen$"}}
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": "erteböllekulturen"}           
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^(?:tidig|mellan|sen)neolitikum$"}}
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": "mellanneolitisk"},
            {"LOWER": "tid"},
            {"LOWER": {"REGEX": r"^[ab]$"}}
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": "trattbägarkulturen"}           
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": "klockbägarkultur"}           
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": "gropkeramisk"},
            {"LOWER": "kultur"}
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": "stridsyxekulturen"}
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"OP": "?", "LOWER": {"REGEX": r"^(?:äldre|yngre)$"}},
            {"LOWER": "bronsålder"}
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"OP": "?", "LOWER": {"REGEX": r"^(?:äldre|förromersk|romersk|yngre)$"}},
            {"LOWER": {"REGEX": r"^järnåldern?$"}}
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": "folkvandringstid"}
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": "vendeltid"}
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": "vikingatid"}
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": "historisk"},
            {"LOWER": "tid"}            
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^medeltida?$"}}
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": "tidig"},
            {"LOWER": "medeltid"}            
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^(?:hög|sen)medeltid$"}}
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": "folkungatiden"}                  
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": "kalmarunionen"}                  
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^(?:tidig|sen)?modern$"}},
            {"LOWER": "tid"}            
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"OP": "?", "LOWER": {"REGEX": r"^(?:äldre|yngre)$"}},
            {"LOWER": "vasatiden"}                  
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": "karolinska"},
            {"LOWER": "tiden"}            
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": "stormaktstiden"}                  
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": "frihetstiden"}                  
        ] 
    }
]