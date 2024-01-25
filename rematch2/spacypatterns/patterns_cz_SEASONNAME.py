"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_cz_SEASONNAME.py
Version :   20240125
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy patterns for use with EntityRuler pipeline components            
Imports :   
Example :           
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
History :   25/01/2024 CFB Initially created script
=============================================================================
"""
patterns_cz_SEASONNAME = [
    {
        # Spring
        "id": "http://vocab.getty.edu/aat/300133097",
        "label": "SEASONNAME",
        "pattern": [{"LOWER": {"REGEX": r"^jar(o|ře)$"}}]
    },
    {
        # Summer
        "id": "http://vocab.getty.edu/aat/300133099",
        "label": "SEASONNAME",
        "pattern": [{"LOWER": "létě"}]
    },
    {
        # Autumn
        "id": "http://vocab.getty.edu/aat/300133093",
        "label": "SEASONNAME",
        "pattern": [{"LOWER": "podzim"}]
    },
    {
        # Winter
        "id": "https://vocab.getty.edu/aat/300133101",
        "label": "SEASONNAME",
        "pattern": [{"LOWER": {"REGEX": r"^zim[aě]$"}}]
    }
]
