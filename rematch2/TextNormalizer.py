"""
=============================================================================
Package :   rematch2
Module  :   TextNormalizer.py
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   ATRIUM
Summary :   spaCy custom pipeline components for text normalisation -
            this can improve subsequent NLP tokenisation and NER results            
Imports :   regex, spacy, Doc, Pipe, Language
Example :   nlp.add_pipe("normalize_text", before = "tagger")
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History :   
20/06/2025 CFB adapted from StringCleaning.py, for use as pipeline components
16/07/2025 CFB now single factory function 'normalize_text' with options
=============================================================================
"""
import regex
from typing import Tuple
from spacy.tokens import Doc
from spacy.pipeline import Pipe
from spacy.language import Language

substitute_spelling_en: list[Tuple[str,str]] = [
    # US English -> English spelling
    # retaining potential capitalisation
    (r"\b(a)rcheo", r"\1rchaeo"),  
    (r"\b(p)aleo", r"\1alaeo"),
    (r"\b(d)efense(s)?\b", r"\1efence\2"),
    (r"\b(c)olor(s)?\b", r"\1olour\2"),
    (r"\b(p)alestra(s)?\b", r"\1alaestra\2"),
    (r"\b(m)ediaeval\b", r"\1edieval"), 
    (r"(\w+)ization\b", r"\1isation"),
    (r"(\w+)izing\b", r"\1ising"),
    (r"(\w+)ized\b", r"\1ised"),
    (r"\b(j)ewelry\b", r"\1ewellery"),
    (r"\b(a)rtifact(s)?\b", r"\1rtefact\2"),
    (r"\b(p)low(s)?\b", r"\1lough\2"),
    (r"\b(g)ray\b", r"\1rey"),
    (r"\b(s)ulfate\b", r"\1ulphate"),
    (r"\b(s)ulfur\b", r"\1ulphur"),
    (r"\b(t)heater(s)?\b", r"\1heatre\2"),
    (r"\b(m)odel(s)?\b", r"\1odel\2"),
    (r"\b(m)odeled\b", r"\1odelled"),
    (r"\b(m)odeling\b", r"\1odelling"),
    (r"\b(h)arbor(s)?\b", r"\1arbour\2"),
    (r"\b(l)abor\b", r"\1abour"),
    (r"\b(a)luminum\b", r"\1luminium")
]

substitute_ligatures_en: list[Tuple[str,str]] = [
    # convert ligatures
    ("ﬀ", "ff"),
    ("ﬁ", "fi"),
    ("ﬂ", "fl"),
    ("ﬃ", "ffi"),
    ("ﬄ", "ffl"),
    ("ﬅ", "ft"),
    ("ﬆ", "st"),
    ("Ꜳ", "AA"),
    ("Æ", "AE"),
    ("ꜳ", "aa")
]

substitute_punctuation_en: list[Tuple[str,str]] = [
    # any dash character to single standard hyphen
    (r"\b\s*(\p{Dash_Punctuation})\s*(?=[^\p{Number}])", " - "),
    (r"\b(\p{Dash_Punctuation})\b", " - "),
    # spacing before/after slashes
    (r"\b\s*([\\\/])\s*\b", r" \1 "),
    # spacing before/after brackets
    (r"([^\s])\s*(\p{Open_Punctuation})\s*([^\s])", r"\1 \2\3"),
    (r"([^\s])\s*(\p{Close_Punctuation})\s*([^\s])", r"\1\2 \3"),        
    # convert ampersands (&) to "and"
    (r"(\p{Letter})\s+&\s+(\p{Letter})", r"\1 and \2"),
    # removing apostrophes
    (r"(\p{Letter})'s\s(\p{Letter})", r"\1s \2"),        
    (r"(\p{Letter}s)'\s(\p{Letter})", r"\1 \2"),
    # spacing after commas
    (r"(\p{Letter}),(\p{Letter})", r"\1, \2")
]

substitute_whitespace_en: list[Tuple[str,str]] = [
    # words hyphenated at line break -
    # remove both hyphen and newline character
    # typical of text extracted from PDF docs
    (r"\p{Dash_Punctuation}\p{Separator}*[\r\n]([a-z])", r"\1"),
    # remove newline characters unless at end of a sentence
    (r"([^.])\p{Separator}*[\r\n]", r"\1 "),
    # convert multi-whitespace to single space (preserving line-breaks)
    (r"\p{Separator}+", " ")
]


class TextNormalizer(Pipe):
    
    def __init__(self, nlp: Language, subs: list[Tuple[str,str]]):
        self.nlp = nlp
        self.subs = {regex.compile(key, regex.IGNORECASE | regex.MULTILINE): val for (key, val) in (subs or [])}         
        

    def __call__(self, doc: Doc) -> Doc:
        text = doc.text
        
        # perform text replacement for each of the subs
        for pattern, val in self.subs.items(): 
            text = pattern.sub(val, text)
               
        # retokenize and return the Doc
        disabled = self.nlp.select_pipes(disable=["ner", "normalize_text"])
        #newDoc = self.nlp.make_doc(text) # this doesnt do lemmas or pos
        newDoc = self.nlp(text)
        newDoc.user_data = doc.user_data.copy()  # copy user data from original doc
        disabled.restore()
        return newDoc
        

@Language.factory(
    name="normalize_text", 
    default_config={
        "normalize_spelling": True,
        "normalize_whitespace": True, 
        "normalize_punctuation": True,
        "supplementary_subs": []
    }) 
def normalize_text_en(
    nlp: Language, 
    name: str="normalize_text",
    normalize_spelling: bool=True,
    normalize_ligatures: bool=True,
    normalize_whitespace: bool=True, 
    normalize_punctuation: bool=True,
    supplementary_subs: list[Tuple[str,str]]=[]) -> Pipe:

    substitutions: list[Tuple[str,str]] = [] 
    substitutions.extend(substitute_whitespace_en if normalize_whitespace else [])
    substitutions.extend(substitute_punctuation_en if normalize_punctuation else [])
    substitutions.extend(substitute_spelling_en if normalize_spelling else [])
    substitutions.extend(substitute_ligatures_en if normalize_ligatures else [])
    substitutions.extend(supplementary_subs)

    return TextNormalizer(nlp, subs=substitutions)


# to run directly, run with -m from package root to enable relative imports to work
# i.e. /workspaces/rematch2 $ python -m rematch2.TextNormalizer
if __name__ == "__main__":   
    import spacy
    
    # usage example
    text = f"archeological  work indi-\ncated  an Iron Age/ Romano- British  /Roman\npost -hole, in( low -lying)ground.\nThis  was  near(vandal-\nized)\n  Mediaeval/post-medieval(15th-17th century? )foot-\nings. Items of Mediaeval &  paleolithic(archeological)jewelry were  located in the New Harbor area.  Gray colored  & oxidized,aluminum artifacts were   found near the theater."
    
    # Note: order can make a difference, so fix
    # whitespace & punctuation before spelling
    nlp = spacy.load("en_core_web_sm", disable=["ner"]) 
    nlp.add_pipe("normalize_text", before = "tagger", config= {"normalize_spelling": False})
        
    print(f"\nBefore:\n\"{text}\"")
    doc = nlp(text)
    print(f"\nAfter:\n\"{doc.text}\"")   
    