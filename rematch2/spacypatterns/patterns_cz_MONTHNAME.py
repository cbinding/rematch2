"""
=============================================================================
Package :   rematch2.spacypatterns
Module  :   patterns_cz_MONTHNAME.py
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
patterns_cz_MONTHNAME = [
    {
        # Jan
        "id": "http://vocab.getty.edu/aat/300410290",
        "label": "MONTHNAME",
        "pattern": [{"LOWER": {"REGEX": r"^led(en|n[ua])$"}}]
    },
    {
        # Feb
        "id": "http://vocab.getty.edu/aat/300410291",
        "label": "MONTHNAME",
        "pattern": [{"LOWER": {"REGEX": r"^únor[ua]?$"}}]
    },
    {
        # Mar
        "id": "http://vocab.getty.edu/aat/300410292",
        "label": "MONTHNAME",
        "pattern": [{"LOWER": {"REGEX": r"^brez(en|n[ua])$"}}]
    },
    {
        # Apr
        "id": "http://vocab.getty.edu/aat/300410293",
        "label": "MONTHNAME",
        "pattern": [{"LOWER": {"REGEX": r"^dub(en|n[ua])$"}}]
    },
    {
        # May
        "id": "http://vocab.getty.edu/aat/300410294",
        "label": "MONTHNAME",
        "pattern": [{"LOWER": {"REGEX": r"^květ(en|n[ua])$"}}]
    },
    {
        # Jun
        "id": "http://vocab.getty.edu/aat/300410295",
        "label": "MONTHNAME",
        "pattern": [{"LOWER": {"REGEX": r"^červ(en|n[ua])$"}}]
    },
    {
        # Jul
        "id": "http://vocab.getty.edu/aat/300410296",
        "label": "MONTHNAME",
        "pattern": [{"LOWER": {"REGEX": r"^červen(ec|c[ie])$"}}]
    },
    {
        # Aug
        "id": "http://vocab.getty.edu/aat/300410297",
        "label": "MONTHNAME",
        "pattern": [{"LOWER": {"REGEX": r"^srp(en|n[ua])$"}}]
    },
    {
        # Sep
        "id": "http://vocab.getty.edu/aat/300410298",
        "label": "MONTHNAME",
        "pattern": [{"LOWER": "září"}]
    },
    {
        # Oct
        "id": "http://vocab.getty.edu/aat/300410299",
        "label": "MONTHNAME",
        "pattern": [{"LOWER": {"REGEX": r"^	říj(en|n[ua])$"}}]
    },
    {
        # Nov
        "id": "http://vocab.getty.edu/aat/300410300",
        "label": "MONTHNAME",
        "pattern": [{"LOWER": {"REGEX": r"^listopadu?$"}}]
    },
    {
        # Dec
        "id": "http://vocab.getty.edu/aat/300410301",
        "label": "MONTHNAME",
        "pattern": [{"LOWER": {"REGEX": r"^prosin(ec|c[ie])$"}}]
    }
]
