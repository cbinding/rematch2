"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_fr_PERIOD.py
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
patterns_fr_PERIOD = [
    {
        "label": "PERIODOLD",
        "pattern": [{"LOWER": "trias"}]
    },
    {
        "label": "PERIODOLD",
        "pattern": [{"LOWER": "secondaire"}]
    },
    {
        "label": "PERIODOLD",
        "pattern": [{"LOWER": "jurassique"}]
    },
    {
        "label": "PERIODOLD",
        "pattern": [{"LOWER": "crétacé"}]
    },
    {
        "label": "PERIODOLD",
        "pattern": [{"LOWER": "tertiaire"}]
    },
    {
        "label": "PERIODOLD",
        "pattern": [{"LOWER": {"REGEX": "^oligoc[eè]ne$"}}]
    },
    {
        "label": "PERIODOLD",
        "pattern": [{"LOWER": {"REGEX": "^plioc[eè]ne$"}}]
    },
    {
        "label": "PERIODOLD",
        "pattern": [{"LOWER": "quaternaire"}]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^pl[eé]istoc[eè]ne$"}},
            {"OP": "?", "LOWER": {
                        "REGEX": "^(ancien|moyen|sup[eé]rieur)$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [{"LOWER": {"REGEX": "pr[ée]histoire"}}]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER":  {"REGEX": "^pal[eé]olithique$"}},
            {"OP": "?", "LOWER": {
                        "REGEX": "^(inf[ée]rieur|moyen|sup[eé]rieur)$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER":  "chronologie"},
            {"OP": "?", "LOWER": {"REGEX": "^am[eé]ricaine$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^b[oö]lling$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^epipal[eé]olithique$"}},
            {"OP": "?", "POS": "ADJ"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^w[uü]rm$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": "dryas"},
            {"OP": "?", "POS": "ADJ"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^aller[oö]d$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^holoc[eè]ne$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": "tardiglaciaire"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^m[eé]solithique$"}},
            {"OP": "?", "LOWER": {"REGEX": "^(ancien|moyen|final|r[ée]cent)$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^n[eé]olithique$"}},
            {"OP": "?", "LOWER": {
                "REGEX": "^(ancien|moyen|final|r[ée]cent|pr[eé]c[eé]ramique)$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^pr[eé]bor[eé]al$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": "atlantique"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^sub\\-bor[eé]al$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": "egypte"},
            {"LOWER": "antique"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": "chronologie"},
            {"LOWER": "antillaise"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": "chalcolithique"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": "protohistoire"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^[aâ]ges?$"}},
            {"LOWER": "des"},
            {"LOWER": {"REGEX": "^métaux$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^(l[’'])?[aâ]ge$"}},
            {"LOWER": "du"},
            {"LOWER": "bronze"},
            {"OP": "?", "LOWER": {"REGEX": "^(ancien|moyen|final)$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": "bronze"},
            {"LOWER": {"REGEX": "^(ancien|moyen|final)$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": "bronze"},
            {"LOWER": {"REGEX": "^r[eé]cent$"}},
            {"OP": "?", "LOWER": {"REGEX": "^i{1,3}$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": {"REGEX": "^myc[eé]nienne$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": "hallstatt"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": "orientalisante"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^sub\\-atlantique$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"OP": "?", "LOWER": {
                "REGEX": "^(premier|deuxi[eè]me|1er|2e|second)$"}},
            {"LOWER": {"REGEX": "^[aâ]ge$"}},
            {"LOWER": "du"},
            {"LOWER": "fer"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": "italie"},
            {"LOWER": {"REGEX": "^archa[iï]que$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": "riss"},
            {"LOWER": "-"},
            {"LOWER": {"REGEX": "^w[uü]rm$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": {"REGEX": "^archa[iï]que$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": "transition"},
            {"LOWER": "bronze"},
            {"LOWER": "/"},
            {"LOWER": "fer"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "antiquit[eé]"}},
            {"OP": "?", "LOWER": {
                "REGEX": "^(grecque|gallo-romaine|gréco-romaine|romaine|tardive)$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^(empire|gallo|r[eé]publique|gaule)$"}},
            {"LOWER": {"REGEX": "^romaine?$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": {"REGEX": "^pr[eé]\\-classique$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": "classique"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": {"REGEX": "^[eé]trusque$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": "la"},
            {"LOWER":  {"REGEX": "t[eè]ne"}},
            {"OP": "?", "LOWER": {"REGEX": "^(i{1,3}|finale)$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": {"REGEX": "^hell[eé]nistique$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": "tardo"},
            {"LOWER": "-"},
            {"LOWER": {"REGEX": "^r[eé]publicaine$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^(haut|bas)$"}},
            {"OP": "?", "POS": "PUNCT"},
            {"LOWER": "empire"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": "haut-empire"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": "bas-empire"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": "empire"},
            {"LOWER": "d'"},
            {"LOWER": "occident"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^r[eè]gne$"}},
            {"LOWER": "d'"},
            {"LOWER": "auguste"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": "franque"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": "empire"},
            {"LOWER": "byzantin"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": {"REGEX": "^m[eé]rovingienne$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": {"REGEX": "^carolingien(ne)?$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^(haut|bas)$"}},
            {"LOWER": "moyen"},
            {"LOWER": {"REGEX": "^[aâ]ge$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^(haut|bas)$"}},
            {"LOWER": "moyen"},
            {"ORTH": "-"},
            {"LOWER": {"REGEX": "^[aâ]ge$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": "moyen"},
            {"LOWER": {"REGEX": "^[aâ]ge$"}},
            {"LOWER": "classique"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": {"REGEX": "m[eé]di[eé]vaux"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^[eé]p(oque)?$"}},
            {"LOWER": "islamique"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": "umayyades"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": "abbassides"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": "empire"},
            {"LOWER": "ottoman"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": "temps"},
            {"LOWER": "modernes"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^p[eé]riode$"}},
            {"LOWER": "moderne"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": "renaissance"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^r[eé]volution$"}},
            {"LOWER": {"REGEX": "^fran[cç]aise$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "contemporaine"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^si[eè]cles$"}},
            {"LOWER": "des"},
            {"LOWER": " l'Industrie"}
        ]
    },



    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"IN": [
                "turonien",
                "gallo-romaine",
                "gallo-romaines"
            ]}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"POS": "ADJ"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "du"},
            {"POS": "PROPN"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": "protohistorique"},
            {"OP": "?", "POS": "ADJ"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^tib[eè]re$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": "antonins"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "s[eé]v[eè]res"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^(julio|tibero)$"}},
            {"OP": "?", "POS": "PUNCT"},
            {"LOWER": "claudiens"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": {"REGEX": "^m[eé]rovingienne$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": {"REGEX": "^carolingien(ne)?$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": {"REGEX": "^archa[iï]que$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "georgienne"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "victorienne"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": {"REGEX": "^hell[eé]nistique$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": {"REGEX": "^august[eé]enne$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": {"REGEX": "^tib[eé]rienne$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "claudienne"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": {"REGEX": "^n[eé]ronienne$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "flavienne"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "de"},
            {"LOWER": "vespasien"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "de"},
            {"LOWER": "domitien"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "de"},
            {"LOWER": "trajan"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "d'hadrien"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "antonine"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": {"REGEX": "aur[eé]lienne"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": {"REGEX": "s[eé]v[eé]rienne"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "de"},
            {"LOWER": "gallein"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "des"},
            {"LOWER": "t[eé]trarques"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "constantinienne"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"OP": "?", "LOWER": {"REGEX": "^([eé]p|[eé]poque|p[eé]riode)$"}},
            {"LOWER": "byzantine"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": {"REGEX": "^si[eè]cle$"}},
            {"LOWER": "des"},
            {"LOWER": {"REGEX": "^lumi[eè]res$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": "minoen"},
            {"OP": "?", "LOWER": {"REGEX": "^(ancien|moyen|r[eé]cent)$"}}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": "subminoen"}
        ]
    },
    {
        "label": "PERIODOLD",
        "pattern": [
            {"LOWER": "corinthien"},
            {"OP": "?", "LOWER": {"REGEX": "^(ancien|moyen|r[eé]cent)$"}}
        ]
    }
]
