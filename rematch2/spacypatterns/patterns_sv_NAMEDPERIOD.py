patterns_sv_NAMEDPERIOD = [ 
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": "paleolitikum"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": "förhistorisk"},
            {"LOWER": "tid"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"OP": "?", "LOWER": {"REGEX": r"^(?:äldre|yngre)$"}},
            {"LOWER": {"REGEX": r"^stenåldern?"}}
                     
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^(?:tidig|mellan|sen)mesolitikum$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^(?:magle|konge)mosekulturen$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": "erteböllekulturen"}           
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^(?:tidig|mellan|sen)neolitikum$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": "mellanneolitisk"},
            {"LOWER": "tid"},
            {"LOWER": {"REGEX": r"^[ab]$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": "trattbägarkulturen"}           
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": "klockbägarkultur"}           
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": "gropkeramisk"},
            {"LOWER": "kultur"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": "stridsyxekulturen"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"OP": "?", "LOWER": {"REGEX": r"^(?:äldre|yngre)$"}},
            {"LOWER": "bronsålder"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"OP": "?", "LOWER": {"REGEX": r"^(?:äldre|förromersk|romersk|yngre)$"}},
            {"LOWER": {"REGEX": r"^järnåldern?$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": "folkvandringstid"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": "vendeltid"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": "vikingatid"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": "historisk"},
            {"LOWER": "tid"}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^medeltida?$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": "tidig"},
            {"LOWER": "medeltid"}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^(?:hög|sen)medeltid$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": "folkungatiden"}                  
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": "kalmarunionen"}                  
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^(?:tidig|sen)?modern$"}},
            {"LOWER": "tid"}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"OP": "?", "LOWER": {"REGEX": r"^(?:äldre|yngre)$"}},
            {"LOWER": "vasatiden"}                  
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": "karolinska"},
            {"LOWER": "tiden"}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": "stormaktstiden"}                  
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": "frihetstiden"}                  
        ] 
    }
]