"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_fr_NAMEDPERIOD.py
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
patterns_fr_NAMEDPERIOD = [
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [{"LOWER": "trias"}]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [{"LOWER": "secondaire"}]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [{"LOWER": "jurassique"}]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [{"LOWER": "crétacé"}]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [{"LOWER": "tertiaire"}]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [{"LOWER": {"REGEX": "^oligoc[eè]ne$"}}]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [{"LOWER": {"REGEX": "^plioc[eè]ne$"}}]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [{"LOWER": "quaternaire"}]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^pl[eé]istoc[eè]ne$"}},
            {"OP": "?", "LOWER": {
                        "REGEX": "^(ancien|moyen|sup[eé]rieur)$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [{"LOWER": {"REGEX": "pr[ée]histoire"}}]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER":  {"REGEX": "^pal[eé]olithique$"}},
            {"OP": "?", "LOWER": {
                        "REGEX": "^(inf[ée]rieur|moyen|sup[eé]rieur)$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER":  "chronologie"},
            {"OP": "?", "LOWER": {"REGEX": "^am[eé]ricaine$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^b[oö]lling$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^epipal[eé]olithique$"}},
            {"OP": "?", "POS": "ADJ"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^w[uü]rm$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": "dryas"},
            {"OP": "?", "POS": "ADJ"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^aller[oö]d$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^holoc[eè]ne$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": "tardiglaciaire"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^m[eé]solithique$"}},
            {"OP": "?", "LOWER": {"REGEX": "^(ancien|moyen|final|r[ée]cent)$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^n[eé]olithique$"}},
            {"OP": "?", "LOWER": {
                "REGEX": "^(ancien|moyen|final|r[ée]cent|pr[eé]c[eé]ramique)$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^pr[eé]bor[eé]al$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": "atlantique"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^sub\\-bor[eé]al$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": "egypte"},
            {"LOWER": "antique"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": "chronologie"},
            {"LOWER": "antillaise"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": "chalcolithique"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": "protohistoire"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^[aâ]ges?$"}},
            {"LOWER": "des"},
            {"LOWER": {"REGEX": "^métaux$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^(l[’'])?[aâ]ge$"}},
            {"LOWER": "du"},
            {"LOWER": "bronze"},
            {"OP": "?", "LOWER": {"REGEX": "^(ancien|moyen|final)$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": "bronze"},
            {"LOWER": {"REGEX": "^(ancien|moyen|final)$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": "bronze"},
            {"LOWER": {"REGEX": "^r[eé]cent$"}},
            {"OP": "?", "LOWER": {"REGEX": "^i{1,3}$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": {"REGEX": "^myc[eé]nienne$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": "hallstatt"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": "orientalisante"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^sub\\-atlantique$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"OP": "*", "ENT_TYPE": "DATEPREFIX"},
            {"OP": "?", "LOWER": {
                "REGEX": "^(premier|deuxi[eè]me|1er|2e|second)$"}},
            {"LOWER": {"REGEX": "^[aâ]ge$"}},
            {"LOWER": "du"},
            {"LOWER": "fer"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": "italie"},
            {"LOWER": {"REGEX": "^archa[iï]que$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": "riss"},
            {"LOWER": "-"},
            {"LOWER": {"REGEX": "^w[uü]rm$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": {"REGEX": "^archa[iï]que$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": "transition"},
            {"LOWER": "bronze"},
            {"LOWER": "/"},
            {"LOWER": "fer"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "antiquit[eé]"}},
            {"OP": "?", "LOWER": {
                "REGEX": "^(grecque|gallo-romaine|gréco-romaine|romaine|tardive)$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^(empire|gallo|r[eé]publique|gaule)$"}},
            {"LOWER": {"REGEX": "^romaine?$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": {"REGEX": "^pr[eé]\\-classique$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": "classique"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": {"REGEX": "^[eé]trusque$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": "la"},
            {"LOWER":  {"REGEX": "t[eè]ne"}},
            {"OP": "?", "LOWER": {"REGEX": "^(i{1,3}|finale)$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": {"REGEX": "^hell[eé]nistique$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": "tardo"},
            {"LOWER": "-"},
            {"LOWER": {"REGEX": "^r[eé]publicaine$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^(haut|bas)$"}},
            {"OP": "?", "POS": "PUNCT"},
            {"LOWER": "empire"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": "haut-empire"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": "bas-empire"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": "empire"},
            {"LOWER": "d'"},
            {"LOWER": "occident"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^r[eè]gne$"}},
            {"LOWER": "d'"},
            {"LOWER": "auguste"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": "franque"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": "empire"},
            {"LOWER": "byzantin"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": {"REGEX": "^m[eé]rovingienne$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": {"REGEX": "^carolingien(ne)?$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^(haut|bas)$"}},
            {"LOWER": "moyen"},
            {"LOWER": {"REGEX": "^[aâ]ge$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^(haut|bas)$"}},
            {"LOWER": "moyen"},
            {"ORTH": "-"},
            {"LOWER": {"REGEX": "^[aâ]ge$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": "moyen"},
            {"LOWER": {"REGEX": "^[aâ]ge$"}},
            {"LOWER": "classique"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": {"REGEX": "m[eé]di[eé]vaux"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": "islamique"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": "umayyades"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": "abbassides"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": "empire"},
            {"LOWER": "ottoman"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": "temps"},
            {"LOWER": "modernes"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^p[eé]riode$"}},
            {"LOWER": "moderne"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": "renaissance"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^r[eé]volution$"}},
            {"LOWER": {"REGEX": "^fran[cç]aise$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "contemporaine"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^si[eè]cles$"}},
            {"LOWER": "des"},
            {"LOWER": " l'Industrie"}
        ]
    },



    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"IN": [
                "turonien",
                "gallo-romaine",
                "gallo-romaines"
            ]}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"POS": "ADJ"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "du"},
            {"POS": "PROPN"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": "protohistorique"},
            {"OP": "?", "POS": "ADJ"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^tib[eè]re$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": "antonins"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "s[eé]v[eè]res"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^(julio|tibero)$"}},
            {"OP": "?", "POS": "PUNCT"},
            {"LOWER": "claudiens"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": {"REGEX": "^m[eé]rovingienne$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": {"REGEX": "^carolingien(ne)?$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": {"REGEX": "^archa[iï]que$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "georgienne"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "victorienne"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": {"REGEX": "^hell[eé]nistique$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": {"REGEX": "^august[eé]enne$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": {"REGEX": "^tib[eé]rienne$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "claudienne"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": {"REGEX": "^n[eé]ronienne$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "flavienne"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "de"},
            {"LOWER": "vespasien"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "de"},
            {"LOWER": "domitien"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "de"},
            {"LOWER": "trajan"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "d'hadrien"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "antonine"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": {"REGEX": "aur[eé]lienne"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": {"REGEX": "s[eé]v[eé]rienne"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "de"},
            {"LOWER": "gallein"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "des"},
            {"LOWER": "t[eé]trarques"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "constantinienne"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "byzantine"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^si[eè]cle$"}},
            {"LOWER": "des"},
            {"LOWER": {"REGEX": "^lumi[eè]res$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": "minoen"},
            {"OP": "?", "LOWER": {"REGEX": "^(ancien|moyen|r[eé]cent)$"}}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": "subminoen"}
        ]
    },
    {
        "label": "NAMEDPERIODOLD",
        "pattern": [
            {"LOWER": "corinthien"},
            {"OP": "?", "LOWER": {"REGEX": "^(ancien|moyen|r[eé]cent)$"}}
        ]
    }
]
