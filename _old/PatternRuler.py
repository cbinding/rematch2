"""
=============================================================================
Package :   rematch2.components
Module  :   PatternRuler.py
Version :   20220803
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy custom pipeline component (specialized EntityRuler)
Imports :   os, sys, spacy, EntityRuler, Doc, Language
Example :   N/A - only used as superclass for more specialized components    
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
History :   
03/08/2022 CFB Initially created script
02/02/2023 CFB Added language factory function
=============================================================================
"""
from spacy.pipeline import EntityRuler
from spacy.tokens import Doc
from spacy.language import Language


@Language.factory("pattern_ruler")
def create_pattern_ruler(nlp, name="pattern_ruler", patterns=[]):
    return PatternRuler(nlp, name, patterns)

# PatternRuler is a specialized EntityRuler (at the moment it's not very specialized!)


class PatternRuler(EntityRuler):
    def __init__(self, nlp: Language, name="pattern_ruler", patterns=None) -> None:
        EntityRuler.__init__(
            self,
            nlp=nlp,
            name=name,
            phrase_matcher_attr="LOWER",
            validate=True,
            overwrite_ents=True,
            ent_id_sep="||",
            patterns=patterns
        )

    # in this instance we just call the parent function, but could do more doc processing here
    def __call__(self, doc: Doc) -> Doc:
        EntityRuler.__call__(self, doc)
        return doc
