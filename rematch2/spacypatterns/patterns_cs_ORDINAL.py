"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_cs_ORDINAL.py
Version :   20240125
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy patterns for use with SpanRuler pipeline components   
            some values from http://cokdybysme.net/pdfs/ordinalnumbers.pdf         
Imports :   
Example :           
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
History :   25/01/2024 CFB Initially created script
=============================================================================
"""
patterns_cs_ORDINAL = [
    { 
        "label": "ORDINAL",
		"pattern": [
            {"TEXT": {"REGEX": r"^\d+\.$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"TEXT": {"REGEX": r"^\d+$"}},
            {"TEXT": {"REGEX": r"^\.$"}}
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": "první" #1st
    },
    { 
        "label": "ORDINAL",
		"pattern": "druhý" #2nd
    },
    { 
        "label": "ORDINAL",
		"pattern": "třetí" #3rd
    },
    { 
        "label": "ORDINAL",
		"pattern": "čtvrtý" #4th
    },
    { 
        "label": "ORDINAL",
		"pattern": "pátý" #5th
    },
    { 
        "label": "ORDINAL",
		"pattern": "šestý" #6th
    },    
    { 
        "label": "ORDINAL",
		"pattern": "sedmý" #7th
    },    
    { 
        "label": "ORDINAL",
		"pattern": "osmý" #8th
    },
    { 
        "label": "ORDINAL",
		"pattern": "devátý" #9th
    },
    { 
        "label": "ORDINAL",
		"pattern": "desátý" #10th
    },
    { 
        "label": "ORDINAL",
		"pattern": "jedenáctý" #11th
    },
    { 
        "label": "ORDINAL",
		"pattern": "dvanáctý" #12th
    },
    { 
        "label": "ORDINAL",
		"pattern": "třináctý" #13th
    },
    { 
        "label": "ORDINAL",
		"pattern": "čtrnáctý" #14th
    },
    { 
        "label": "ORDINAL",
		"pattern": "patnáctý" #15th
    },
    { 
        "label": "ORDINAL",
		"pattern": "šestnáctý" #16th
    },
    { 
        "label": "ORDINAL",
		"pattern": "sedmnáctý" #17th
    },
    { 
        "label": "ORDINAL",
		"pattern": "osmnáctý" #18th
    },
    { 
        "label": "ORDINAL",
		"pattern": "devatenáctý" #19th
    },
    { 
        "label": "ORDINAL",
		"pattern": "dvacátý" #20th
    },
    { 
        "label": "ORDINAL",
		"pattern": "dvacátý první" #21st
    },
    { 
        "label": "ORDINAL",
		"pattern": "jedenadvacátý" #21st 
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": "dvacáty"},   
            {"LOWER": "druhý"}  #22nd       
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": "dvaadvacátý"  #22nd   
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": "dvacátý"},
            {"LOWER": "třetí"}   #23rd         
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": "třiadvacátý"  #23rd   
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": "dvacátý"},
            {"LOWER": "čtvrtý"} #24th           
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": "čtyřiadvacátý"  #24th   
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": "dvacátý"},
            {"LOWER": "pátý"} #25th           
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": "pětadvacátý"  #25th   
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": "dvacátý"},
            {"LOWER": "šestý"}  #26th          
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": "šestadvacátý"  #26th   
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": "dvacátý"},
            {"LOWER": "sedmý"} #27th           
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": "sedmadvacátý"  #27th   
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": "dvacátý"},
            {"LOWER": "osmý"} #28th           
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": "osmadvacátý"  #28th   
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": "dvacátý"},
            {"LOWER": "devátý"}  #29th          
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": "devětadvacáty"  #29th   
    },
    { 
        "label": "ORDINAL",
		"pattern": "třicátý" #30th
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": "třicátá"},
            {"LOWER": "první"} #31st           
        ]
    }
]