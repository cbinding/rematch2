patterns_no_DATEPREFIX = [
    { 
        "label": "DATEPREFIX",
        "language": "no", 
        "pattern": [
            {"LOWER": {"REGEX": r"^cir[ck]a$"}}
        ] 
    },
    { 
        "label": "DATEPREFIX", 
        "language": "no",
        "pattern": [
            {"LOWER": {"REGEX": r"^ca\.?$"}}
        ] 
    },
    { 
        "label": "DATEPREFIX",
        "language": "no", 
        "pattern": [
            {"LOWER": "rundt"}
        ] 
    },
    { 
        "label": "DATEPREFIX", 
        "language": "no",
        "pattern": [
            {"LOWER": "omtrent"}
        ] 
    },
    { 
        "label": "DATEPREFIX",
        "language": "no", 
        "pattern": [
            {"LOWER": {"REGEX": r"^(?:[eäæ]ldre|yngre|eldste|tidl?[ei]g)$"}},  
            {"OP": "?", "LOWER": {"REGEX": r"^på$"}}
        ] 
    },    
    { 
        "label": "DATEPREFIX", 
        "language": "no",
        "pattern": [
            {"LOWER": "inngangen"},  
            {"LOWER": "til"}           
        ] 
    },
    { 
        "label": "DATEPREFIX", 
        "language": "no",
        "pattern": [
            {"LOWER": {"REGEX": r"^(begynnelsen|slutten$)"}},  
            {"LOWER": "av"},
            {"OP": "?", "LOWER": "det"}
        ] 
    },    
    { 
        "label": "DATEPREFIX", 
        "language": "no",
        "pattern": [
            {"LOWER": {"REGEX": r"^f[oø]r$"}}
        ] 
    },
    { 
        "label": "DATEPREFIX", 
        "language": "no",
        "pattern": [
            {"LOWER": {"REGEX": r"^(?:i|på)$"}}
        ] 
    },
    { 
        "label": "DATEPREFIX",
        "language": "no", 
        "pattern": [
            {"OP": "?", "LOWER": "i"},
            {"LOWER": "løpet"},
            {"LOWER": "av"}                
        ] 
    },
    { 
        "label": "DATEPREFIX",
        "language": "no", 
        "pattern": [
            {"LOWER": {"REGEX": r"^(?:etter|siden)$"}}
        ] 
    }    
]