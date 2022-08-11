patterns_fr_DATESUFFIX = [
    { 
        "label": "DATESUFFIX", 
        "language": "fr",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": r"cal\.?"}},
            {"LOWER": {"REGEX": r"^(ad|bc|bp|a\.d\.|b\.c\.|b\.p\.)$"}}              
        ]
    },
    { 
        "label": "DATESUFFIX", 
        "language": "fr",
        "pattern": [
            {"LOWER": {"REGEX": r"^(av(\.|ant)?|ap(r\.?|r[eè]s)?)$"}},
            {"LOWER":  {"REGEX": r"^j\.?$"}} ,
            {"LOWER":  {"REGEX": r"^\-?c\.?$"}}            
        ]
    },     
    { 
        "label": "DATESUFFIX", 
        "language": "fr",
        "pattern": [
            {"LOWER": {"REGEX": r"^(av(\.|ant)?|ap(r?\.?|r[eè]s)?)$"}},
            {"LOWER":  "jc"}                
        ]
    }, 
    { 
        "label": "DATESUFFIX", 
        "language": "fr",
        "pattern": [
            {"LOWER": {"REGEX": r"^(av(\.|ant)?|ap(r\.?|r[eè]s)?)$"}},
            {"LOWER":  {"REGEX": r"^j\.-C$"}}           
        ]
    }, 
    { 
        "label": "DATESUFFIX", 
        "language": "fr",
        "pattern": [
            {"LOWER": {"REGEX": r"^(av(\.|ant)?|ap(r\.?|r[eè]s)?)$"}},
            {"LOWER":  {"REGEX": r"^j\.?$"}},
            {"OP": "?", "TEXT":  "-"},
            {"LOWER":  {"REGEX": r"^c\.?$"}}            
        ]
    }, 
    { 
        "label": "DATESUFFIX", 
        "language": "fr",
        "pattern": [
            {"LOWER": {"REGEX":  r"^(av(\.|ant)?|ap(r\.?|r[eè]s)?)$"}},
            {"LOWER": {"REGEX": r"^j\.$"}},
            {"LOWER": {"REGEX": r"^-?c\.$"}}            
        ]
    }, 
    { 
        "label": "DATESUFFIX", 
        "language": "fr",
        "pattern": [
            { "LOWER": "de" },
            { "LOWER": "notre" },
            { "LOWER":  { "REGEX": r"^[eè]re$" }}            
        ]
    },
    { 
        "label": "DATESUFFIX", 
        "language": "fr",
        "pattern": [
            {"LOWER": {"REGEX":  r"^(av(\.|ant)?|ap(r\.?|r[eè]s)?)$"}},
            {"LOWER": {"REGEX": r"^n(\.|otre)$"}},
            {"LOWER":  {"REGEX": r"^[eè]re$"}}            
        ]
    },
    { 
        "label": "DATESUFFIX", 
        "language": "fr",
        "pattern": [
            {"LOWER": {"REGEX":  r"^(av(\.|ant)?|ap(r\.?|r[eè]s)?)$"}},
            {"LOWER": {"REGEX": r"^n\.[eè]$"}}               
        ]
    },  
    { 
        "label": "DATESUFFIX", 
        "language": "fr",
        "pattern": [
            {"LOWER": {"REGEX":  r"^(av(\.|ant)?|ap(r\.?|r[eè]s)?)$"}},
            {"LOWER": {"REGEX": r"^n\.$"}} ,
            {"LOWER": {"REGEX": "^è$"}}               
        ]
    },
    { 
        "label": "DATESUFFIX", 
        "language": "fr",
        "pattern": [
            {"LOWER": "cal"},
            {"OP": "?", "LOWER": "."},
            {"LOWER": {"REGEX": r"^b[cp]$"}}                        
        ]
    }    
]