"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_no_PERIOD.py
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
patterns_no_PERIOD = [ 
    { 
        "label": "PERIOD",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"LOWER": {"REGEX": r"^steinalder(?:en)?$"}}
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"LOWER": {"REGEX": r"^(?:tidlig|mellom|sei?n)(?:mesolitt?iske?|mesol[iuo]tikk?um)$"}}
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"LOWER": {"REGEX": r"^(?:tidlig|mellom|sei?n)(?:neolitt?iske?|neolitikk?um)$"}}
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"LOWER": "metalltid"}
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"LOWER": {"REGEX": r"^brons(?:ea|å|aa?)lder(?:en)?$"}}
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"LOWER": {"REGEX": r"^j[eäæ]rn(?:å|aa?)lder(?:en)?$"}}
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"LOWER": {"REGEX": r"^romer(?:ske?|tid)$"}}
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"LOWER": {"REGEX": r"^folkevandringstid(?:en)?$"}}
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"LOWER": {"REGEX": r"^merovingertid(?:en)?$"}}
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"LOWER": {"REGEX": r"^vikinge?tid(?:en)?$"}}
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^(?:tidlig|høy|sen)?(?:middelalder(?:en)?|medeltida)$"}}
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^(?:nyere|moderne|vår)$"}},
            {"LOWER": {"REGEX": r"^tida?$"}}
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^istid(?:ens?)?$"}}            
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^oldtid(?:ens?)?$"}}            
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": "forhistoriske"}            
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^(?:paleolittiske?|paleolitikum)$"}}            
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^jegersteinalder(?:en)?$"}}            
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": "pionerfase"}            
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^pionerbosetning(?:en)?$"}}            
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^(?:jeger|fosna|komsa)(?:[–-]?kultur(?:en)?)?$"}}            
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^(?:Mikrolittfasen|\bmm\b)$"}}            
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": "tørkopfasen"}            
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^lundev(?:å|aa?)genfasen$"}}            
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^nøstvet(?:fasen)?$"}}             
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^nøstvet(?:[–-]?kultur(?:en)?)?$"}}            
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": "gjølstadfasen"}            
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": "tverrpilfasen"}            
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": "nøstvetøksfasen"}            
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^(?:traktbeger(?:fasen)?|\btrb\b)$"}}            
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": "senstenalder"}            
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": "bondesteinalder"}            
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": "stridsøksfasen"}            
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": "seinneolitikum"}            
        ] 
    },    
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": "germansk"},
            {"LOWER": {"REGEX": r"^j[eäæ]rn(?:å|aa?)lder(?:en)?$"}}            
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": "reformatorisk"}            
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^borgerkrigstid(?:en)?$"}}            
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^mellomkrigstid(?:en)?$"}}            
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": "etter"},
            {"ORTH": {"REGEX": r"^[–-]$"}},        
            {"LOWER": "reformatorisk"}   
        ] 
    },
    { 
        "label": "PERIOD",
		"pattern": [
            {"LOWER": {"REGEX": r"^per(?:iode)?$"}},
            {"LOWER": {"REGEX": r"^[IV]+$"}}              
        ] 
    }
]