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
14/05/2026 CFB Replaced with patterns from SpanScorer.py, removed some redundant patterns
=============================================================================
"""
patterns_en_NEGATION = [
    [{ "LOWER": { "REGEX": "^preclud(e[ds]?|ing)$" }}],
    [{ "LOWER": { "REGEX": "^(lack|scarcity|absence)$" }}, { "LOWER": "of" }],
    [{ "LOWER": { "REGEX": "^(no|lack(s|ed))$" }}, { "LOWER": "evidence" }, { "OP": "?", "LOWER": "of" }],
    [{ "LOWER": "did" }, { "LOWER": "not" }, { "LOWER": "indicate" }],
    [{ "LOWER": "lack" }, { "LOWER": "of" }, { "OP": "?", "LOWER": "evidence" }],
    [{ "LOWER": "not" }, { "LOWER":  { "REGEX": "^(suggest(ed)?|reveal(ed)?|detected)$" }}],
    [{ "LOWER": { "REGEX": "^fail(s|ed)$" }}, { "LOWER": "to"}, {"LOWER": "reveal" }],
    [{ "LOWER": { "REGEX": "^(is|was)$" }}, { "LOWER": "absent" }]
]