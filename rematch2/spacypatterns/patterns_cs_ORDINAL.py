"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_cs_ORDINAL.py
Version :   20240125
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy patterns for use with EntityRuler pipeline components   
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
            {"LOWER": {"REGEX": r"^(1\.|první)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(2\.|druhý)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(3\.|třetí)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(4\.|čtvrtý)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(5\.|pátý)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(6\.|šestý)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": "6."
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(7\.|sedmý)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"TEXT": "7"},  
            {"TEXT": "."},           
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(8\.|osmý)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(9\.|devátý)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(10\.|desátý)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(11\.|jedenáctý)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(12\.|dvanáctý)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(13\.|třináctý)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(14\.|čtrnáctý)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(15\.|patnáctý)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(16\.|šestnáctý)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(17\.|sedmnáctý)$"}}            
        ]
    },
     { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(18\.|osmnáctý)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(19\.|devatenáctý)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(20\.|dvacátý)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(21\.|dvacátý první|jedenadvacátý)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(22\.|dvacáty druhý|dvaadvacátý)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(23\.|dvacátý třetí|třiadvacátý)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(24\.|dvacátý čtvrtý|čtyřiadvacátý)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(25\.|dvacátý pátý|pětadvacátý)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(26\.|dvacátý šestý|šestadvacátý)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(27\.|dvacátý sedmý|sedmadvacátý)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(28\.|dvacátý osmý|osmadvacátý)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(29\.|dvacátý devátý|devětadvacáty)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(30\.|třicátý)$"}}            
        ]
    },
    { 
        "label": "ORDINAL",
		"pattern": [
            {"LOWER": {"REGEX": r"^(31\.|třicátá první)$"}}            
        ]
    }
]