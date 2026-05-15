"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_it_SEASONNAME.py
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
patterns_it_SEASONNAME = [
    { 
        "label": "SEASONNAME",
		"pattern": [
            {"LOWER": {"REGEX": r"^(primavera|estate|autunno|inverno)$"}}            
        ]
    }
]