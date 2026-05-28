"""
=============================================================================
Package :   rematch2
Module  :   BaseMatcher.py
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Summary :   spaCy custom pipeline component (specialized Matcher)
            used in SpanScorer fopr significance and negation proximity scoring, 
            base class for other custom matcher pipeline components
Imports :   spacy, Doc, Span, Matcher, Vocab, Iterable, Any, cast
Example :       
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History :   
14/05/2026 CFB Split out from SpanScorer script                
=============================================================================
"""
from dataclasses import dataclass
import spacy
from spacy.tokens import Doc, Span
from spacy.matcher import Matcher
from spacy.vocab import Vocab
from typing import Iterable, Any, cast

@dataclass(frozen=True)
class Pattern:
    id: str
    label: str
    pattern: str|list[dict]|list[str]
    
    
class BaseMatcher(Matcher):
    def __init__(self, vocab: Vocab, validate: bool=True):
        super().__init__(vocab, validate=validate)        
        
    # Add single word (case-insensitive) pattern for each term in terms
    def add_terms(self, 
        label: str="unknown", 
        term_list: list[str]=[], 
        token_pos: list[str]=[]) -> None:

        pos_test: dict = {}
        if (len(token_pos) > 0):
            pos_test = { "POS": { "IN": token_pos } }            
        
        patterns = []
        for term in term_list:
            pattern: dict = { "LOWER": term.lower() }
            pattern.update(pos_test)
            patterns.append([pattern])  

        self.add(label, patterns)

    # Add patterns passed in (see spaCy matcher pattern syntax)
    def add_patterns(self, label: str="UNKNOWN", patterns: list=[]) -> None:
        self.add(key=label, patterns=patterns)

    def __call__(self, doc: Doc, *args, **kwargs) -> Any:
        # Always receive spans from the base Matcher by forcing as_spans=True.
        # Accept flexible args/kwargs to remain compatible with the base signature.
        kwargs["as_spans"] = True
        matches = super().__call__(doc, *args, **kwargs)
        # remove duplicates and overlaps, keep longest
        matches = spacy.util.filter_spans(cast(Iterable[Span], matches))
        return matches
    

# to test this module independently, run from package root:
# python -m components.BaseMatcher
if __name__ == "__main__":
    patterns = [
        [{ "LOWER": { "REGEX": "^biostratigraph(ic|y)$" }, "POS": "ADJ"}],
        [{ "LOWER": { "REGEX": "^calibrat(ed|ion)$" }}]
    ]
    nlp = spacy.load("en_core_web_sm", disable=['ner'])
    matcher = BaseMatcher(nlp.vocab)   
    matcher.add_patterns("significance", patterns) 
    doc = nlp("The site yielded rich biostratigraphic evidence, and the calibrated dated corroborated the evidence.")
    matches = matcher(doc)  
    print(matches) # returned list of spans
    # [biostratigraphic, calibrated]  