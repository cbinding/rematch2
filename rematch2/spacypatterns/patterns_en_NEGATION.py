"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_en_NEGATION.py
Version :   20240228
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy patterns for use with EntityRuler pipeline components            
Imports :   
Example :           
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
History :   28/02/2024 CFB Initially created script
=============================================================================
"""
patterns_en_NEGATION = [
    { 
        "label": "NEGATION",
		"pattern": "absence of"
    },
    { 
        "label": "NEGATION",
		"pattern": "no correlation"
    },
    { 
        "label": "NEGATION",
		"pattern": "lack of evidence"
    },
    { 
        "label": "NEGATION",
		"pattern": "no evidence"
    }, 
    { 
        "label": "NEGATION",
		"pattern": "little evidence"
    },  
    { 
        "label": "NEGATION",
		"pattern": "no support for"
    }, 
    { 
        "label": "NEGATION",
		"pattern": "does not support"
    },  
    { 
        "label": "NEGATION",
		"pattern": "unlikely"
    },
    { 
        "label": "NEGATION",
		"pattern": "improbable"
    },
    { 
        "label": "NEGATION",
        "pattern": "probably not"
    },
    { 
        "label": "NEGATION",
		"pattern": "not"
    },
    { 
        "label": "NEGATION",
		"pattern": "not possible"
    },
    { 
        "label": "NEGATION",
		"pattern": "impossible"
    },
    { 
        "label": "NEGATION",
		"pattern": "cannot be"
    }
]