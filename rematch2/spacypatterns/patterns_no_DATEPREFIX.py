patterns_no_DATEPREFIX = [
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^cir[ck]a$"}}
        ] 
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^ca\.?$"}}
        ] 
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": "rundt"}
        ] 
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": "omtrent"}
        ] 
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(?:[eäæ]ldre|yngre|eldste|tidl?[ei]g)$"}},  
            {"OP": "?", "LOWER": {"REGEX": r"^på$"}}
        ] 
    },    
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": "inngangen"},  
            {"LOWER": "til"}           
        ] 
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(begynnelsen|slutten$)"}},  
            {"LOWER": "av"},
            {"OP": "?", "LOWER": "det"}
        ] 
    },    
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^f[oø]r$"}}
        ] 
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(?:i|på)$"}}
        ] 
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"OP": "?", "LOWER": "i"},
            {"LOWER": "løpet"},
            {"LOWER": "av"}                
        ] 
    },
    { 
        "label": "DATEPREFIX",
		"pattern": [
            {"LOWER": {"REGEX": r"^(?:etter|siden)$"}}
        ] 
    }    
]