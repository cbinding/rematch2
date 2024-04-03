"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_sv_YEARSPAN.py
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
patterns_sv_YEARSPAN = [ 
        { 
        "label": "YEARSPAN",
		"pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"LOWER": {"REGEX": r"^\d+0\-talet$"}}             
        ] 
    },
    { 
        "label": "YEARSPAN", 
        
        "comment": "",
		"pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"_": {"is_monthname": True}},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "*", "_": {"is_datesuffix": True}},
        ]
    },
    { 
        "label": "YEARSPAN", 
        
        "comment": "",
		"pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}}, 
            {"_": {"is_seasonname": True}},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "*", "_": {"is_datesuffix": True}},
        ]
    },
    { 
        "label": "YEARSPAN", 
        
        "comment": "",
		"pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"_": {"is_datesuffix": True}},
        ] 
    },
    { 
        "label": "YEARSPAN", 
        
        "comment": "",
		"pattern": [
            {"ORTH": {"REGEX": r"^\d+[\–\-]\d+$"}},
            {"OP": "*", "_": {"is_datesuffix": True}}
        ] 
    },
    { 
        "label": "YEARSPAN", 
        
        "comment": "",
		"pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "*", "_": {"is_datesuffix": True}}, 
            {"_": {"is_dateseparator": True}},
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"ORTH": {"REGEX": r"^\d+$"}},
            {"OP": "*", "_": {"is_datesuffix": True}},
        ] 
    },
    { 
        "label": "YEARSPAN",
		"pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"LOWER": {"REGEX": r"^\d+00\-(talet)?$"}},  
            {"_": {"is_dateseparator": True}},
            {"LOWER": {"REGEX": r"^\d+00\-(talet)?$"}},    
            {"OP": "?", "_": {"is_datesuffix": True}},
        ] 
    },
    { 
        "label": "YEARSPAN",         
        "comment": "",
		"pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"_": {"is_ordinal": True}},
            {"LOWER": {"REGEX": r"^(århundradet|årtusendet)$"}},
            {"OP": "*", "_": {"is_datesuffix": True}},
        ]
    },
    { 
        "label": "YEARSPAN",         
        "comment": "",
		"pattern": [
            {"OP": "*", "_": {"is_dateprefix": True}},
            {"_": {"is_ordinal": True}},
            {"OP": "?", "LOWER": {"REGEX": r"^(århundradet|årtusendet)$"}},
            {"OP": "*", "_": {"is_datesuffix": True}},
            {"_": {"is_dateseparator": True}},
            {"OP": "*", "_": {"is_dateprefix": True}}, 
            {"_": {"is_ordinal": True}},
            {"LOWER": {"REGEX": r"^(århundradet|årtusendet)$"}},
            {"OP": "*", "_": {"is_datesuffix": True}}
        ]
    },
    { 
        "label": "YEARSPANXX",
        "comment": "**See https://stackoverflow.com/questions/57477852/spacy-matcher-with-entities-spanning-more-than-a-single-token  retokenizing with custom entity types..",
		"pattern": [
           {"ORTH": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}
        ]
    }
]
