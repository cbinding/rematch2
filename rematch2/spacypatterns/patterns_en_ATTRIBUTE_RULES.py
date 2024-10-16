"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_en_ATTRIBUTE_RULES.py
Version :   20241009
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   ATRIUM
Summary :       
    spaCy patterns to override default attribute_ruler POS tagging
    spaCy POS tagger is statistical and does not always get it right. 
    Correct problematic issues here. These patterns to be added to
    the attribute_ruler component of the pipeline
Imports :   
Example :           
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
History :   09/10/2024 CFB Initially created script
=============================================================================
"""
patterns_en_ATTRIBUTE_RULES = [    
    { 
        # e.g. "Roman mosaic" -> "mosaic" is NOUN, not PROPN
        # "the mosaic" -> "mosaic" is NOUN, not ADJ
        "patterns": [[ 
            { "POS": { "IN": ["ADJ", "DET"] } }, 
            { "POS": { "IN": ["ADJ", "PROPN"] }, "LOWER": "mosaic" } ]],
        "attrs": { "POS": "NOUN" },
        "index": 1
    },    
    { 
        # eg "villa complex" or "villa building" -> "villa" is NOUN, not ADJ
        "patterns": [[ 
            { "LOWER": "villa" }, 
            { "POS": "NOUN" } ]],
        "attrs": { "POS": "NOUN" },
        "index": 0
    },
    { 
        # eg "post-conquest" -> "post" is ADJ, not NOUN
        "patterns": [[ 
            { "POS": "NOUN", "LOWER": "post" }, 
            { "POS": "PUNCT", "TEXT": "-" } ]],
        "attrs": { "POS": "ADJ" },
        "index": 0
    }
]