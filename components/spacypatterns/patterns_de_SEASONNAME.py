"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_de_SEASONNAME.py
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
patterns_de_SEASONNAME = [
    { 
        # Spring
        "id": "http://vocab.getty.edu/aat/300133097",
        "label": "SEASONNAME",
		"pattern": [{"LOWER":"frühling"}]
    },
    {
        # Summer
        "id": "http://vocab.getty.edu/aat/300133099",
        "label": "SEASONNAME",
		"pattern": [{"LOWER": "sommer"}]
    },
    {
        # Autumn
        "id": "http://vocab.getty.edu/aat/300133093",
        "label": "SEASONNAME",
		"pattern": [{"LOWER": "herbst"}]
    },
    {
        # Winter
        "id": "http://vocab.getty.edu/aat/300133101",
        "label": "SEASONNAME",
		"pattern": [{"LOWER": "winter"}]
    },
]