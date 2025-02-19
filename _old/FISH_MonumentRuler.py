"""
=============================================================================
Package :   rematch2
Module  :   FISH_MonumentRuler.py
Version :   20220803
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy custom pipeline component (specialized EntityRuler)
Imports :   os, sys, spacy, EntityRuler, Doc, Language
Example :   nlp.add_pipe("fish_monument_ruler", last=True);
            draws on https://github.com/ICLRandD/Blackstone/blob/master/blackstone/pipeline/concepts.py            
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
History :   03/08/2022 CFB Initially created script
=============================================================================
"""
import os
import sys
import spacy            # NLP library

from spacy.language import Language
# from spacy.lang.de import German
# from spacy.lang.fr import French

from spacy.pipeline import EntityRuler
from spacy.tokens import Doc

# from collections import Counter
# from patterns import patterns_de_MONUMENT
from ..spacypatterns import patterns_en_FISH_MONUMENT
# from patterns import patterns_fr_MONUMENT
from spacy.pipeline import EntityRuler

# module_path = os.path.abspath(os.path.join('..', 'src'))
# if module_path not in sys.path:
# sys.path.append(module_path)

# defaults to English patterns if no language-specific factory exists


@Language.factory("fish_monument_ruler")
def create_fish_monument_ruler(nlp, name="fish_monument_ruler", patterns=patterns_en_FISH_MONUMENT):
    return EntityRuler(
        nlp=nlp,
        name=name,
        phrase_matcher_attr="LOWER",
        validate=True,
        overwrite_ents=True,
        ent_id_sep="||",
        patterns=patterns
    )


# test the FISH_MonumentRuler pipeline component
if __name__ == "__main__":
    import json
    test_file_name = "test-examples.json"
    tests = []
    with open(test_file_name, "r") as f:  # what if file doesn't exist?
        tests = json.load(f)

    for test in tests:
        print(f"-------------\nlanguage = {test['language']}")

        nlp = spacy.load(test["pipe"], disable=['ner'])
        # nlp.max_length = 2000000

        nlp.add_pipe("fish_monument_ruler", last=True)
        print(nlp.pipe_names)
        doc = nlp(test["text"])

        for ent in doc.ents:
            print(ent.ent_id_, ent.text, ent.label_)
