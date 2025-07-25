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
import regex # using regex (not re) to allow for e.g. \p{Dash_Punctuation}
from typing import Tuple
from spacy.tokens import Doc
from spacy.pipeline import Pipe
from spacy.language import Language
from typing import Optional
from dataclasses import dataclass

@dataclass(frozen=True)
class Substitution:
    find: str
    repl: str
    ignoreCase: Optional[bool] = True

# text substitutions to normalize spelling (English)
substitute_spelling_en: list[Substitution] = [
    # US English -> English spelling
    # retaining potential capitalisation
    Substitution(r"\b(a)rcheo", r"\1rchaeo"),  
    Substitution(r"\b(p)aleo", r"\1alaeo"),
    Substitution(r"\b(d)efense(s)?\b", r"\1efence\2"),
    Substitution(r"\b(c)olor(s)?\b", r"\1olour\2"),
    Substitution(r"\b(p)alestra(s)?\b", r"\1alaestra\2"),
    Substitution(r"\b(m)ediaeval\b", r"\1edieval"), 
    Substitution(r"(\w+)ization\b", r"\1isation"),
    Substitution(r"(\w+)izing\b", r"\1ising"),
    Substitution(r"(\w+)ized\b", r"\1ised"),
    Substitution(r"\b(j)ewelry\b", r"\1ewellery"),
    Substitution(r"\b(a)rtifact(s)?\b", r"\1rtefact\2"),
    Substitution(r"\b(p)low(s)?\b", r"\1lough\2"),
    Substitution(r"\b(g)ray\b", r"\1rey"),
    Substitution(r"\b(s)ulfate\b", r"\1ulphate"),
    Substitution(r"\b(s)ulfur\b", r"\1ulphur"),
    Substitution(r"\b(t)heater(s)?\b", r"\1heatre\2"),
    Substitution(r"\b(m)odel(s)?\b", r"\1odel\2"),
    Substitution(r"\b(m)odeled\b", r"\1odelled"),
    Substitution(r"\b(m)odeling\b", r"\1odelling"),
    Substitution(r"\b(h)arbor(s)?\b", r"\1arbour\2"),
    Substitution(r"\b(l)abor\b", r"\1abour"),
    Substitution(r"\b(a)luminum\b", r"\1luminium")
]


# text substitutions to normalize ligatures (English)
substitute_ligatures_en: list[Substitution] = [
    # convert ligatures
    Substitution("ﬀ", "ff"),
    Substitution("ﬁ", "fi"),
    Substitution("ﬂ", "fl"),
    Substitution("ﬃ", "ffi"),
    Substitution("ﬄ", "ffl"),
    Substitution("ﬅ", "ft"),
    Substitution("ﬆ", "st"),
    Substitution("ß", "s"),
    Substitution("Ꜳ", "AA", False),
    Substitution("ꜳ", "aa", False),    
    Substitution("Æ", "AE", False),
    Substitution("æ", "ae", False),   
    Substitution("Œ", "OE", False),     
    Substitution("œ", "oe", False)    
]


# text substitutions to normalize punctuation (English)
substitute_punctuation_en: list[Substitution] = [
    # any dash character to single standard hyphen
    Substitution(r"\b\s*(\p{Dash_Punctuation})\s*(?=[^\p{Number}])", " - "),
    Substitution(r"\b(\p{Dash_Punctuation})\b", " - "),
    # spacing before/after slashes
    Substitution(r"\b\s*([\\\/])\s*\b", r" \1 "),
    # spacing before/after brackets
    Substitution(r"([^\s])\s*(\p{Open_Punctuation})\s*([^\s])", r"\1 \2\3"),
    Substitution(r"([^\s])\s*(\p{Close_Punctuation})\s*([^\s])", r"\1\2 \3"),        
    # convert ampersands (&) to "and"
    Substitution(r"(\p{Letter})\s+&\s+(\p{Letter})", r"\1 and \2"),
    # removing apostrophes
    Substitution(r"(\p{Letter})'s\s(\p{Letter})", r"\1s \2"),        
    Substitution(r"(\p{Letter}s)'\s(\p{Letter})", r"\1 \2"),
    # spacing after commas
    Substitution(r"(\p{Letter}),(\p{Letter})", r"\1, \2")
]


# text substitutions to normalize whitespace (English)
substitute_whitespace_en: list[Substitution] = [
    # words hyphenated at line break -
    # remove both hyphen and newline character
    # typical of text extracted from PDF docs
    Substitution(r"\p{Dash_Punctuation}\p{Separator}*[\r\n]([a-z])", r"\1"),
    # remove newline characters unless at end of a sentence
    Substitution(r"([^.])\p{Separator}*[\r\n]", r"\1 "),
    # convert multi-whitespace to single space (but preserving line-breaks)
    Substitution(r"\p{Separator}+", " ")
]


# spaCy pipeline class to perform the text normalisation using substitutions
class TextNormalizer(Pipe):    

    @staticmethod
    def _compileSub(sub: Substitution) -> Substitution:
        flags = regex.IGNORECASE | regex.MULTILINE if sub.ignoreCase else regex.MULTILINE
        return Substitution(regex.compile(sub.find, flags), sub.repl, sub.ignoreCase)        

    def __init__(self, nlp: Language, subs: list[Substitution] = []):
        self.nlp: Language = nlp
        self.substitutions: list[Substitution] = list(map(self._compileSub, subs))
         
    def __call__(self, doc: Doc) -> Doc:
        text = doc.text
        
        # perform text replacement for each of the substitutions
        for substitution in self.substitutions:
            text = substitution.find.sub(substitution.repl, text)
               
        # retokenize and return the Doc
        disabled = self.nlp.select_pipes(disable=["ner", "normalize_text"])
        #newDoc = self.nlp.make_doc(text) # note this doesn't do lemmas or pos, only tokenisation
        newDoc = self.nlp(text)
        newDoc.user_data = doc.user_data.copy()  # copy user data from original doc        
        disabled.restore()
        return newDoc
                

# Note currently English specific but this script is extensible 
# to add substitutions for other languages
@Language.factory(
    name="normalize_text", 
    default_config={
        "normalize_spelling": True,
        "normalize_ligatures": True,
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
    supplementary_subs: list[Substitution]=[]) -> Pipe:

    substitutions: list[Substitution] = [] 
    # order can make a difference, so whitespace, punctuation & ligatures before spelling        
    substitutions.extend(substitute_whitespace_en if normalize_whitespace else [])
    substitutions.extend(substitute_punctuation_en if normalize_punctuation else [])
    substitutions.extend(substitute_ligatures_en if normalize_ligatures else [])    
    substitutions.extend(substitute_spelling_en if normalize_spelling else [])
    substitutions.extend(supplementary_subs)
    # redo whitespace substitution to ensure normalized after all other subs have run
    substitutions.extend(substitute_whitespace_en if normalize_whitespace else [])
    
    return TextNormalizer(nlp, substitutions)


# to run this script directly for testing, run with -m from package root to ensure
# relative imports work i.e. /workspaces/rematch2 $ python -m rematch2.TextNormalizer
if __name__ == "__main__":   
    import spacy
    
    # usage example - testing whitespace & punctuation issues and inconsistent spelling
    text = f"archeological  work indi-\ncated   an Iron Age/ Romano- British  /Roman\npost -hole, in( low -lying)ground.\nThis  was  near(vandal-\nized)\n  mediæval/post-medieval(15th-17th century? )foot-\nings. Items of Mediaeval &  paleolithic(archeological)jewelry dated to the 2nd -  3rd century and pottery & vertebræ of a fœtus were  located in the New Harbor area.  Gray colored  & oxidized,aluminum artifacts were   found near the theater."
    
    nlp = spacy.load("en_core_web_sm", disable=["ner"]) 
    nlp.add_pipe("normalize_text", before="tagger")
    #nlp.add_pipe("normalize_text", before="tagger", config={"normalize_spelling": False})
        
    print(f"\nBefore:\n\"{text}\"")
    doc = nlp(text)
    print(f"\nAfter:\n\"{doc.text}\"")   
    