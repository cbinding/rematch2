patterns_fr_NAMEDPERIOD = [
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [{"LOWER": "trias"}]
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [{"LOWER": "secondaire"}]
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [{"LOWER": "jurassique"}]
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [{"LOWER": "crétacé"}]
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [{"LOWER": "tertiaire"}]
    },
    { 
        "label": "NAMEDPERIOD",
        "language": "fr", 
        "pattern": [{"LOWER": {"REGEX": "^oligoc[eè]ne$"}}]
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [{"LOWER": {"REGEX": "^plioc[eè]ne$"}}]
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [{"LOWER": "quaternaire"}]
    },
    { 
        "label": "NAMEDPERIOD",
        "language": "fr", 
        "pattern": [
            {"LOWER": {"REGEX": "^pl[eé]istoc[eè]ne$"}},
            {"OP": "?", "LOWER": {"REGEX": "^(ancien|moyen|sup[eé]rieur)$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [{"LOWER": {"REGEX": "pr[ée]histoire"}}]
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER":  {"REGEX": "^pal[eé]olithique$"}},
            {"OP": "?", "LOWER": {"REGEX": "^(inf[ée]rieur|moyen|sup[eé]rieur)$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER":  "chronologie"},
            {"OP": "?", "LOWER": {"REGEX": "^am[eé]ricaine$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": {"REGEX": "^b[oö]lling$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": {"REGEX": "^epipal[eé]olithique$"}},
            {"OP": "?", "POS": "ADJ"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": {"REGEX": "^w[uü]rm$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": "dryas"},
            {"OP": "?", "POS": "ADJ"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": {"REGEX": "^aller[oö]d$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": {"REGEX": "^holoc[eè]ne$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": "tardiglaciaire"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": {"REGEX": "^m[eé]solithique$"}},
            {"OP": "?", "LOWER": {"REGEX": "^(ancien|moyen|final|r[ée]cent)$"}}        
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": {"REGEX": "^n[eé]olithique$"}}, 
            {"OP": "?", "LOWER": {"REGEX": "^(ancien|moyen|final|r[ée]cent|pr[eé]c[eé]ramique)$"}} 
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": {"REGEX": "^pr[eé]bor[eé]al$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": "atlantique"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": {"REGEX": "^sub\\-bor[eé]al$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": "egypte"},
            {"LOWER": "antique"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": "chronologie"},
            {"LOWER": "antillaise"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": "chalcolithique"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": "protohistoire"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": {"REGEX": "^[aâ]ges?$"}}, 
            {"LOWER": "des"}, 
            {"LOWER": {"REGEX": "^métaux$"}}                      
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": {"REGEX": "^(l[’'])?[aâ]ge$"}}, 
            {"LOWER": "du"}, 
            {"LOWER": "bronze"},
            {"OP": "?", "LOWER": {"REGEX": "^(ancien|moyen|final)$"}}                  
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": "bronze"},
            {"LOWER": {"REGEX": "^(ancien|moyen|final)$"}}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
        "language": "fr", 
        "pattern": [
            {"LOWER": "bronze"},
            {"LOWER": {"REGEX": "^r[eé]cent$"}},
            {"OP": "?", "LOWER": {"REGEX": "^i{1,3}$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": {"REGEX": "^[eé]p(oque)?$"}},   
            {"LOWER": {"REGEX": "^myc[eé]nienne$"}}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": "hallstatt"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": {"REGEX": "^[eé]p(oque)?$"}},   
            {"LOWER": "orientalisante"}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": {"REGEX": "^sub\\-atlantique$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"}, 
            {"OP": "?", "LOWER": {"REGEX": "^(premier|deuxi[eè]me|1er|2e|second)$"}}, 
            {"LOWER": {"REGEX": "^[aâ]ge$"}}, 
            {"LOWER": "du"}, 
            {"LOWER": "fer"}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": "italie"},   
            {"LOWER": {"REGEX": "^archa[iï]que$"}}           
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": "riss"},
            {"LOWER": "-"},  
            {"LOWER": {"REGEX": "^w[uü]rm$"}}         
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": {"REGEX": "^archa[iï]que$"}}           
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": "transition"},
            {"LOWER": "bronze"},
            {"LOWER": "/"},
            {"LOWER": "fer"}           
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": {"REGEX": "antiquit[eé]"}},  
            {"OP": "?", "LOWER": {"REGEX": "^(grecque|gallo-romaine|gréco-romaine|romaine|tardive)$"}}                      
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": {"REGEX": "^(empire|gallo|r[eé]publique|gaule)$"}}, 
            {"LOWER": {"REGEX": "^romaine?$"}}           
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": {"REGEX": "^pr[eé]\\-classique$"}}           
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER":"classique"}           
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": {"REGEX": "^[eé]trusque$"}}           
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": "la"}, 
            {"LOWER":  {"REGEX": "t[eè]ne"}},
            {"OP": "?", "LOWER": {"REGEX": "^(i{1,3}|finale)$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": {"REGEX": "^hell[eé]nistique$"}}           
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": "tardo"},
            {"LOWER": "-"},
            {"LOWER": {"REGEX": "^r[eé]publicaine$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": {"REGEX": "^(haut|bas)$"}}, 
            {"OP": "?", "POS": "PUNCT"},
            {"LOWER": "empire"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": "haut-empire"}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": "bas-empire"}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": "empire"},
            {"LOWER": "d'"}, 
            {"LOWER": "occident"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": {"REGEX": "^r[eè]gne$"}}, 
            {"LOWER": "d'"}, 
            {"LOWER": "auguste"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": "franque"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": "empire"},
            {"LOWER": "byzantin"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": {"REGEX": "^m[eé]rovingienne$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": {"REGEX": "^carolingien(ne)?$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^(haut|bas)$"}},
            {"LOWER": "moyen"}, 
            {"LOWER": {"REGEX": "^[aâ]ge$"}}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^(haut|bas)$"}}, 
            {"LOWER": "moyen"}, 
            {"ORTH": "-"}, 
            {"LOWER": {"REGEX": "^[aâ]ge$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": "moyen"}, 
            {"LOWER": {"REGEX": "^[aâ]ge$"}},
            {"LOWER": "classique"}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": {"REGEX": "m[eé]di[eé]vaux"}}
        ] 
    },  
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": "islamique"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": "umayyades"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": "abbassides"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": "empire"},
            {"LOWER": "ottoman"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": "temps"},
            {"LOWER": "modernes"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
        "language": "fr", 
        "pattern": [
            {"LOWER": {"REGEX": "^p[eé]riode$"}},
            {"LOWER": "moderne"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": "renaissance"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD",
        "language": "fr", 
        "pattern": [
            {"LOWER": {"REGEX": "^r[eé]volution$"}},
            {"LOWER": {"REGEX": "^fran[cç]aise$"}}
        ] 
    },     
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},   
            {"LOWER": "contemporaine"}            
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "language": "fr",
        "pattern": [
            {"LOWER": {"REGEX": "^si[eè]cles$"}},
            {"LOWER": "des"},    
            {"LOWER": " l'Industrie"}            
        ] 
    },



    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            { "LOWER": { "IN": [
                "turonien",
                "gallo-romaine", 
                "gallo-romaines"            
            ]}}
        ] 
    },    
    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            {"LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}}, 
            {"POS": "ADJ"}
        ]
    },
    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            {"LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "du"},  
            {"POS": "PROPN"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            {"LOWER": "protohistorique"},
            {"OP": "?", "POS": "ADJ"}   
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            {"LOWER": {"REGEX": "^tib[eè]re$"}}
        ] 
    },    
    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            {"LOWER": "antonins"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            {"LOWER": {"REGEX": "s[eé]v[eè]res"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            {"LOWER": {"REGEX": "^(julio|tibero)$"}},
            {"OP": "?", "POS": "PUNCT"},
            {"LOWER": "claudiens"}
        ] 
    },    
    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": {"REGEX": "^m[eé]rovingienne$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": {"REGEX": "^carolingien(ne)?$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": {"REGEX": "^archa[iï]que$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "georgienne"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "victorienne"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": {"REGEX": "^hell[eé]nistique$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": {"REGEX": "^august[eé]enne$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": {"REGEX": "^tib[eé]rienne$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "claudienne"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": {"REGEX": "^n[eé]ronienne$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "flavienne"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "de"},
            {"LOWER": "vespasien"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "de"},
            {"LOWER": "domitien"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "de"},
            {"LOWER": "trajan"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "d'hadrien"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "antonine"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": {"REGEX": "aur[eé]lienne"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": {"REGEX": "s[eé]v[eé]rienne"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "de"},
            {"LOWER": "gallein"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "des"},
            {"LOWER": "t[eé]trarques"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "constantinienne"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "byzantine"}
        ] 
    },   
    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            {"LOWER": {"REGEX": "^si[eè]cle$"}}, 
            {"LOWER": "des"}, 
            {"LOWER": {"REGEX": "^lumi[eè]res$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            {"LOWER": "minoen"}, 
            {"OP": "?", "LOWER": {"REGEX": "^(ancien|moyen|r[eé]cent)$"}}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            {"LOWER": "subminoen"}
        ] 
    },
    { 
        "label": "NAMEDPERIOD", 
        "pattern": [
            {"LOWER": "corinthien"}, 
            {"OP": "?", "LOWER": {"REGEX": "^(ancien|moyen|r[eé]cent)$"}}
        ] 
    }   
]     