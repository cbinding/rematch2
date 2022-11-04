"""
=============================================================================
Package :   rematch2.components
Module  :   EvidenceRuler.py
Version :   20220803
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   ARIADNEplus
Summary :   spaCy custom pipeline component (specialized EntityRuler)
            to identify Terms from the HE Evidence Thesaurus 
            in free text. Entity type added will be "EVIDENCE"
Imports :   os, sys, spacy, Language, PatternRuler
Example :   nlp.add_pipe("evidence_ruler", last=True)           
License :   https://creativecommons.org/licenses/by/4.0/ [CC-BY]
History :   03/08/2022 CFB Initially created script
=============================================================================
"""
import os
import sys
import spacy            # NLP library

from spacy.language import Language
from ..patterns import patterns_en_EVIDENCE

from .PatternRuler import PatternRuler

# defaults to English patterns if no language-specific factory exists


@Language.factory("evidence_ruler")
def create_evidence_ruler(nlp, name="evidence_ruler", patterns=patterns_en_EVIDENCE):
    return PatternRuler(nlp, name, patterns)


# test the EvidenceRuler class
if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm", disable=['ner'])
    nlp.add_pipe("evidence_ruler", last=True)
    print(nlp.pipe_names)
    text = "Undertook some excavation on the site, then some aerial reconnaissance, followed by a laser scanning survey."
    doc = nlp(text)
    for ent in doc.ents:
        print(ent.ent_id_, ent.text, ent.label_)
