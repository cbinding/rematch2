"""
=============================================================================
Package :   rematch2
Module  :   FISH_ArchScienceRuler.py
Version :   20220803
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy custom pipeline component (specialized EntityRuler)
            to identify Terms from the FISH Archaeological Sciences Thesaurus 
            in free text. Entity type added will be "ARCHSCIENCE"
Imports :   os, sys, spacy, Language, EntityRuler
Example :   nlp.add_pipe("fish_archscience_ruler", last=True)           
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
History :   03/08/2022 CFB Initially created script
=============================================================================
"""
import os
import sys
import spacy            # NLP library

from spacy.language import Language
from ..spacypatterns import patterns_en_FISH_ARCHSCIENCE

from spacy.pipeline import EntityRuler

# module_path = os.path.abspath(os.path.join('..', 'src'))
# if module_path not in sys.path:
# sys.path.append(module_path)

# defaults to English patterns if no language-specific factory exists


@Language.factory("fish_archscience_ruler")
def create_fish_archscience_ruler(nlp, name="fish_archscience_ruler", patterns=patterns_en_FISH_ARCHSCIENCE):
    return EntityRuler(
        nlp=nlp,
        name=name,
        phrase_matcher_attr="LOWER",
        validate=True,
        overwrite_ents=True,
        ent_id_sep="||",
        patterns=patterns
    )


# test the FISH_ArchScienceRuler class
if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm", disable=['ner'])
    nlp.add_pipe("fish_archscience_ruler", last=True)
    print(nlp.pipe_names)
    text = "Undertook some alpha spectrometry followed by a stable isotope analysis, on the site."
    doc = nlp(text)
    for ent in doc.ents:
        print(ent.ent_id_, ent.text, ent.label_)
