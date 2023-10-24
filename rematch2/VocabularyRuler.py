"""
=============================================================================
Package :   rematch2.components
Module  :   VocabularyRuler.py
Version :   20231010
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   ARIADNEplus
Summary :   spaCy custom pipeline component (specialized EntityRuler)
Imports :   EntityRuler, Language
Example :   N/A - superclass for more specialized components    
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
History :   
10/10/2023 CFB Added language factory function
=============================================================================
"""
import json
import os
import sys
from pathlib import Path
import spacy
from spacy.pipeline import EntityRuler
from spacy.tokens import Doc
from spacy.language import Language
from pprint import pprint


@Language.factory("vocabulary_ruler", default_config={
    "lemmatize": True,         # whether to lemmatize vocabulary terms
    "pos": [],                  # POS to include in pattern
    "min_term_length": 3,       # min term length to make a pattern for
    "min_lemmatize_length": 4,  # min term length to lemmatize
    "default_label": "UNKNOWN",  # label to tag identified terms
    "default_language": "en",   # language of term
    "vocab": []})               # vocabulary terms - expects [{"id": "123", "term": "xyz"}, {"id": "234", "term": "abc"}]
def create_vocabulary_ruler(nlp,
                            name: str,
                            lemmatize: bool,
                            pos,
                            min_term_length: int,
                            min_lemmatize_length: int,
                            default_label: str,
                            default_language: str,
                            vocab):

    return VocabularyRuler(nlp,
                           name=name,
                           lemmatize=lemmatize,
                           pos=pos,
                           min_term_length=min_term_length,
                           min_lemmatize_length=min_lemmatize_length,
                           default_label=default_label,
                           default_language=default_language,
                           vocab=vocab)


class VocabularyRuler(EntityRuler):

    def __init__(self,
                 nlp: Language,
                 name: str,
                 lemmatize: bool,
                 pos,
                 min_term_length: int,
                 min_lemmatize_length: int,
                 default_label: str,
                 default_language: str,
                 vocab) -> None:

        EntityRuler.__init__(
            self,
            nlp=nlp,
            name=name,
            phrase_matcher_attr="LOWER",
            validate=False,
            overwrite_ents=True,
            ent_id_sep="||"
        )

        # add terms from vocab as generated patterns
        # vocab: [{id, term}, {id, term}]
        # patterns: [{id, label, language, term, pattern}, {id, label, language, term, pattern}]
        patterns = []
        for item in vocab:
            # clean input values before using
            clean_id = item.get("id", "").strip()
            clean_label = item.get("label", default_label).strip()
            clean_language = item.get("language", default_language).strip()
            clean_term = item.get("term", "").strip()

            # don't use if term length < min_term_length
            if (len(clean_term) < min_term_length):
                continue

            # add cleaned values to new pattern object
            pattern = VocabularyRuler._term_to_pattern(
                nlp, clean_term, lemmatize, min_lemmatize_length, pos)

            patterns.append({
                "id": clean_id,
                "label": clean_label,
                "language": clean_language,
                "term": clean_term,
                "pattern":  pattern
            })
        # pprint(patterns)
        self.add_patterns(patterns)

    def __call__(self, doc: Doc) -> Doc:
        EntityRuler.__call__(self, doc)
        return doc

    # lemmatize each word in phrase for better chance of free-text match
    # using SAME nlp pipeline for patterns and terms being compared,
    # rather than separate independent tokenisation..
    @staticmethod
    def _term_to_pattern(nlp, term="", lemmatize=False, min_lemmatize_length=4, pos=[]):
        # normalise whitespace and force lowercase
        # (lemmatization won't work if capitalised)
        clean = ' '.join(term.strip().lower().split())
        doc = nlp(clean)
        # lem = ' '.join(tok.lemma_ for tok in doc)
        pattern = []
        phrase_length = len(doc)
        term_length = len(term)

        for n, tok in enumerate(doc, 1):
            pat = {}

            # lemmatize term if required, and if
            # { "LEMMA": "board" } or { "LOWER": "board" }

            if (lemmatize and term_length >= min_lemmatize_length):
                pat["LEMMA"] = tok.lemma_
            else:
                pat["LOWER"] = tok.text

            # add any required pos tags if passed in
            # note POS only applied to LAST term if multi-word phrase
            # e.g. "skirting boards" { "LEMMA": "board", "POS": "NOUN"}
            if (len(pos) > 0 and n == phrase_length):
                pat["POS"] = {"IN": pos}  # ",".join(pos)

            # if (lemmatize):
                # pat = { "LEMMA": tok.lemma_ }
            # else:
                # pat = { "LOWER": tok.text }
            pattern.append(pat)

        # pat = [{"LEMMA": tok.lemma_} for tok in doc]
        # e.g. {"LEMMA": "tools", "POS": "NOUN"}
        return pattern


# test the VocabularyRuler class
if __name__ == "__main__":

    # sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    # from rematch2.components.spacypatterns import vocab_en_AAT_OBJECTS
    # from ..spacypatterns import vocab_en_AAT_OBJECTS

    test_text = '''
        Aside from three residual flints, none closely datable, the earliest remains comprised a small assemblage of Roman pottery \
        and ceramic building material, also residual and most likely derived from a Roman farmstead found immediately to the north \
        within the Phase II excavation area. A single sherd of Anglo-Saxon grass-tempered pottery was also residual. The earliest \
        features, which accounted for the majority of the remains on site, relate to medieval agricultural activity focused within \
        a large enclosure. There was little to suggest domestic occupation within the site: the pottery assemblage was modest and \
        well abraded, whilst charred plant remains were sparse, and, as with some metallurgical residues, point to waste disposal \
        rather than the locations of processing or consumption. A focus of occupation within the Rodley Manor site, on higher ground \
        160m to the north-west, seems likely, with the currently site having lain beyond this and providing agricultural facilities, \
        most likely corrals and pens for livestock. Animal bone was absent, but the damp, low-lying ground would have been best suited \
        to cattle. An assemblage of medieval coins recovered from the subsoil during a metal detector survey may represent a dispersed hoard.
        '''    

    # reading vocab from JSON file instead. This WORKS...
    # no need for python modules for what should be JSON input
    # and don't need specialised pipelines, only vocabulary_ruler
    vocab = []
    vocab_dir = (Path(__file__).parent / "vocabularies").resolve()
    file_path = os.path.join(
        vocab_dir, "vocab_en_AAT_ACTIVITIES_20231018.json")
    # print(file_path)

    with open(file_path, "r") as f:  
        # print(f)
        vocab = json.load(f)

    nlp = spacy.load("en_core_web_sm", disable=['ner'])

    nlp.add_pipe("vocabulary_ruler", last=True, config={
        "min_lemmatize_length": 4,
        "min_term_length": 3,
        "lemmatize": True,
        # "pos": ["NOUN"],
        # "pos": ["VERB"],
        "default_label": "OBJECT",
        "default_language": "en",
        "vocab": vocab
    })

    doc = nlp(test_text)

    for ent in doc.ents:
        print(ent.ent_id_, ent.text, ent.label_)

    # for tok in doc:
        # print(tok.text, tok.pos_, tok.lemma_)
