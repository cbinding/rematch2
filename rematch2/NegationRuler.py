"""
=============================================================================
Package :   rematch2
Module  :   NegationRuler.py
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy custom pipeline component (specialized SpanRuler)
            Language-sensitive component to identify negation phrases
            in free text. span label added will be "NEGATION"
Imports :   os, sys, spacy, Language, SpanRuler, Doc
Example :   nlp.add_pipe("negation_ruler", last=True)           
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History :   
28/02/2024 CFB Initially created script
28/03/2024 CFB base on SpanRuler instead of EntityRuler
=============================================================================
"""
import os
import sys
from pathlib import Path
import json
import spacy            # NLP library
from spacy.pipeline import SpanRuler
from spacy.language import Language
from spacy.lang.en import English
from spacy.tokens import Doc, Span

if __package__ is None or __package__ == '':
    # uses current directory visibility
    from spacypatterns import *
    from Util import *
    from SpanPairs import SpanPairs
    from DocSummary import DocSummary    
else:
    # uses current package visibility
    from .spacypatterns import *
    from .Util import * 
    from .SpanPairs import SpanPairs    
    from .DocSummary import DocSummary


# NegationRuler is a specialized SpanRuler
class NegationRuler(SpanRuler):

    def __init__(self, nlp: Language, name: str="negation_ruler", patterns: list=[]) -> None:
        normalized_patterns = normalize_patterns(
            nlp=nlp, 
            patterns=patterns,
            default_label="NEGATION",
            lemmatize=False,
            min_term_length=2
        )        

        SpanRuler.__init__(
            self,
            nlp=nlp,        
            name=name,
            spans_key="custom",
            phrase_matcher_attr="LOWER",
            validate=False,
            overwrite=False
        )
        
        # add negation patterns to this pipeline component
        self.add_patterns(normalized_patterns)
        # print(normalized_patterns)   
        # add extension property to Span
        Span.set_extension(name="is_negated", default=False, force=True)     
    
    
    def __call__(self, doc: Doc) -> Doc:
        doc = SpanRuler.__call__(self, doc)
        all_spans = doc.spans.get("custom",[])
        
        # flag any negated spans
        # get list of unique labels of all spans in current doc (remove 'NEGATION')
        unique_labels = list(set(map(lambda span: span.label_, all_spans)))
        if "NEGATION" in unique_labels: unique_labels.remove("NEGATION")

        # get negation pairs for ALL unique labels
        rel_ops = [ "<", ">", "<<", ">>", ".", ";"]              
        span_pairs = SpanPairs(doc=doc, rel_ops=rel_ops, left_labels=["NEGATION"], right_labels=unique_labels).pairs        
        negated_span_starts = list(map(lambda pair: pair.span2.start, span_pairs))
        
        # flag spans as is_negated 
        # (TODO: take scores into account?)        
        for span in all_spans:
            if span.start in negated_span_starts:
                span._.is_negated = True
           
        return doc


@Language.factory("negation_ruler", default_config={"patterns": []})
def create_negation_ruler(nlp: Language, name: str = "negation_ruler", patterns: list=[]) -> NegationRuler:
    return NegationRuler(nlp, name, patterns)


@English.factory("negation_ruler")
def create_negation_ruler_en(nlp: Language, name: str = "negation_ruler") -> NegationRuler:
    return create_negation_ruler(nlp, name, patterns_en_NEGATION)

'''
# patterns for other languages not yet implemented
@Spanish.factory("negation_ruler")
def create_negation_ruler_es(nlp: Language, name: str = "negation_ruler") -> NegationRuler:
    return create_negation_ruler(nlp, name, patterns_es_NEGATION)


@French.factory("negation_ruler")
def create_negation_ruler_fr(nlp: Language, name: str = "negation_ruler") -> NegationRuler:
    return create_negation_ruler(nlp, name, patterns_fr_NEGATION)


@Italian.factory("negation_ruler")
def create_negation_ruler_it(nlp: Language, name: str = "negation_ruler") -> NegationRuler:
    return create_negation_ruler(nlp, name, patterns_it_NEGATION)


@Dutch.factory("negation_ruler")
def create_negation_ruler_nl(nlp: Language, name: str = "negation_ruler") -> NegationRuler:
    return create_negation_ruler(nlp, name, patterns_nl_NEGATION)


@Norwegian.factory("negation_ruler")
def create_negation_ruler_no(nlp: Language, name: str = "negation_ruler") -> NegationRuler:
    return create_negation_ruler(nlp, name, patterns_no_NEGATION)


@Swedish.factory("negation_ruler")
def create_negation_ruler_sv(nlp: Language, name: str = "negation_ruler") -> NegationRuler:
    return create_negation_ruler(nlp, name, patterns_sv_NEGATION)

# Polish as temp experimental substitute until Czech is available
@Polish.factory("negation_ruler")
def create_negation_ruler_cs(nlp: Language, name: str = "negation_ruler") -> NegationRuler:
    return create_negation_ruler(nlp, name, patterns_cs_NEGATION)
'''

# test the NegationRuler class
if __name__ == "__main__":
    tests = []
    # load some local test texts from JSON file..    
    test_file_path = (Path(__file__).parent.parent / "test_examples_english.json").resolve()    
    with open(test_file_path, "r") as f:
        tests = json.load(f)
    
    # set up the spaCy pipeline
    nlp = get_pipeline_for_language("en")
    nlp.add_pipe("negation_ruler", last=True)
        
    # run using test texts
    for test in tests:
        text = test.get("text", "")
        
        print(f"-------------\n{text}\n")
        doc = nlp(text)
        
        print("Tokens:\n" + DocSummary(doc).tokens("text"))
        print("Spans:\n" + DocSummary(doc).spans("text"))

