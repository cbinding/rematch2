"""
=============================================================================
Package   : rematch2
Module    : ChildSpanRemover.py
Classes   : child_span_remover
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Project   : 
Summary   : Filter out spans contained by other spans 
            e.g. "IRON AGE" within "LATE IRON AGE"
Imports   : spacy, Doc, Language, DEFAULT_SPANS_KEY
Example   : nlp.add_pipe("child_span_remover", last=True)
        or doc = child_span_remover(doc, spans_key=DEFAULT_SPANS_KEY)
License   : https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History
07/01/2024 CFB Initially created script
13/05/2026 CFB StopWordRemover removed; test script improved
=============================================================================
"""
import spacy
from spacy.tokens import Doc
from spacy.language import Language
from .Util import DEFAULT_SPANS_KEY

# removes spans contained by other spans
@Language.component("child_span_remover")
def child_span_remover(doc: Doc, spans_key: str=DEFAULT_SPANS_KEY) -> Doc:
    spans = doc.spans.get(spans_key, [])    
    doc.spans[spans_key] = spacy.util.filter_spans(spans)
    return doc

# testing the component
if __name__ == "__main__":
    nlp: Language = spacy.blank("en")    
    text = "the quick brown fox jumps over the lazy dog"
    doc: Doc = nlp(text)
    print(f"\"{doc}\"")
    w = doc[3:4] # "fox"
    x = doc[1:3] # "quick brown"
    y = doc[1:4] # "quick brown fox"
    z = doc[4:5] # "jumps"
    doc.spans[DEFAULT_SPANS_KEY] = [w, x, y, z]  
    print(f"Before: {doc.spans[DEFAULT_SPANS_KEY]}")   
    doc = child_span_remover(doc, spans_key=DEFAULT_SPANS_KEY)
    print(f"After: {doc.spans[DEFAULT_SPANS_KEY]}") 
    '''Output:
    "the quick brown fox jumps over the lazy dog"
    Before: [fox, quick brown, quick brown fox, jumps]
    After: [quick brown fox, jumps]
    '''
        