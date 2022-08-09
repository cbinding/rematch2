patterns_nl_DATEPREFIX = [
    { 
        "label": "DATEPREFIX", 
        "language": "nl",
        "pattern": [
            {"LOWER": {"REGEX": r"^(ca\.?|ongeveer)$"}}            
        ]
    },
    {
        "label": "DATEPREFIX", 
        "language": "nl",
        "pattern": [
            {"LOWER": {"REGEX": r"^(vroege?|begin|midden|eind|laat|late)$"}}            
        ]
    },    
    { 
        "label": "DATEPREFIX",
        "language": "nl", 
        "pattern": [
            {"LOWER": {"REGEX": r"^(eerste|tweede)$"}},
            {"LOWER": "helft"}
        ]
    },
    { 
        "label": "DATEPREFIX", 
        "language": "nl",
        "pattern": [
            {"LOWER": {"REGEX": r"^(eerste|tweede|derde|vierde)$"}},
            {"LOWER": {"REGEX": r"kwart(ier|aal)?"}}           
        ]
    }    
]