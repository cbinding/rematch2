patterns_no_NAMEDPERIOD = [ 
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"LOWER": {"REGEX": r"^steinalder(?:en)?$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"LOWER": {"REGEX": r"^(?:tidlig|mellom|sei?n)(?:mesolitt?iske?|mesol[iuo]tikk?um)$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"LOWER": {"REGEX": r"^(?:tidlig|mellom|sei?n)(?:neolitt?iske?|neolitikk?um)$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"LOWER": "metalltid"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"LOWER": {"REGEX": r"^brons(?:ea|å|aa?)lder(?:en)?$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"LOWER": {"REGEX": r"^j[eäæ]rn(?:å|aa?)lder(?:en)?$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"LOWER": {"REGEX": r"^romer(?:ske?|tid)$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"LOWER": {"REGEX": r"^folkevandringstid(?:en)?$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"LOWER": {"REGEX": r"^merovingertid(?:en)?$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"LOWER": {"REGEX": r"^vikinge?tid(?:en)?$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^(?:tidlig|høy|sen)?(?:middelalder(?:en)?|medeltida)$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^(?:nyere|moderne|vår)$"}},
            {"LOWER": {"REGEX": r"^tida?$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^istid(?:ens?)?$"}}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^oldtid(?:ens?)?$"}}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": "forhistoriske"}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^(?:paleolittiske?|paleolitikum)$"}}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^jegersteinalder(?:en)?$"}}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": "pionerfase"}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^pionerbosetning(?:en)?$"}}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^(?:jeger|fosna|komsa)(?:[–-]?kultur(?:en)?)?$"}}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^(?:Mikrolittfasen|\bmm\b)$"}}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": "tørkopfasen"}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^lundev(?:å|aa?)genfasen$"}}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^nøstvet(?:fasen)?$"}}             
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^nøstvet(?:[–-]?kultur(?:en)?)?$"}}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": "gjølstadfasen"}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": "tverrpilfasen"}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": "nøstvetøksfasen"}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^(?:traktbeger(?:fasen)?|\btrb\b)$"}}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": "senstenalder"}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": "bondesteinalder"}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": "stridsøksfasen"}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": "seinneolitikum"}            
        ] 
    },    
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": "germansk"},
            {"LOWER": {"REGEX": r"^j[eäæ]rn(?:å|aa?)lder(?:en)?$"}}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": "reformatorisk"}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^borgerkrigstid(?:en)?$"}}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^mellomkrigstid(?:en)?$"}}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": "etter"},
            {"ORTH": {"REGEX": r"^[–-]$"}},        
            {"LOWER": "reformatorisk"}   
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^per(?:iode)?$"}},
            {"LOWER": {"REGEX": r"^[IV]+$"}}              
        ] 
    }
]