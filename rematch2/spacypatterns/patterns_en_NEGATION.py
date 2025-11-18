"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_en_NEGATION.py
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy patterns for use with SpanRuler pipeline components            
Imports :   
Example :           
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
History :   
28/02/2024 CFB Initially created script
10/06/2025 CFB Reduced to tightly focused list according to negation-review-2025h.docx
=============================================================================
"""
patterns_en_NEGATION = [
    { 
        "id": "no",
        "label": "NEGATION",
		"pattern": [
            {"LOWER": "no"},
            #{"IS_PUNCT": False, "OP": r"?="}
        ]
    },
    { 
        "id": "not_detected",
        "label": "NEGATION",
		"pattern": "not detected"
    },
    { 
        "id": "no_evidence",
        "label": "NEGATION",
		"pattern": "no evidence"
    },
    { 
        "id": "lack_of_evidence",
        "label": "NEGATION",
		"pattern": "lack of evidence"
    },
    { 
        "id": "lacks_evidence",
        "label": "NEGATION",
		"pattern": "lacks evidence"
    },
    { 
        "id": "lacked_evidence",
        "label": "NEGATION",
		"pattern": "lacked evidence"
    },
    { 
        "id": "lack_of",
        "label": "NEGATION",
		"pattern": "lack of"
    },
    { 
        "id": "scarcity_of",
        "label": "NEGATION",
		"pattern": "scarcity of"
    },
    { 
        "id": "absence_of",
        "label": "NEGATION",
		"pattern": "absence of"
    },
    { 
        "id": "not_suggest",
        "label": "NEGATION",
		"pattern": "not suggest"
    },
    { 
        "id": "not_reveal",
        "label": "NEGATION",
		"pattern": "not reveal"
    },
    { 
        "id": "fails_to_reveal",
        "label": "NEGATION",
		"pattern": "fails to reveal"
    },
    { 
        "id": "failed_to_reveal",
        "label": "NEGATION",
		"pattern": "failed to reveal"
    },
    { 
        "id": "is_absent",
        "label": "NEGATION",
		"pattern": "is absent"
    },
    { 
        "id": "precluded",
        "label": "NEGATION",
		"pattern": "precluded"
    },
    { 
        "id": "preclude",
        "label": "NEGATION",
		"pattern": "preclude"
    },
    { 
        "id": "precludes",
        "label": "NEGATION",
		"pattern": "precludes"
    }
]