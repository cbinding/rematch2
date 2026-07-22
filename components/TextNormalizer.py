"""
=============================================================================
Package :   rematch2
Module  :   TextNormalizer.py
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   ATRIUM
Summary :   spaCy custom pipeline components for text normalisation;
            this can improve subsequent NLP tokenisation and IE results            
Imports :   regex, spacy, Doc, Pipe, Language, dataclass
Example :   nlp.add_pipe("text_normalizer", first=True)
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History :   
20/06/2025  CFB adapted from StringCleaning.py, to use as pipeline component
16/07/2025  CFB now single factory function with options for spelling, 
                ligatures, whitespace and punctuation normalisation
11/08/2025  CFB added decode_unicode option to allow for unicode characters
                to be converted to ASCII equivalents (e.g. accents removed)
14/05/2026  CFB fix support for regex patterns in substitutions
22/07/2026  CFB refactored substitutions for (future) multilingual support
=============================================================================
"""
import regex # using regex (not re) to allow for e.g. \p{Dash_Punctuation}
from unidecode import unidecode # for removing accents from characters
#from typing import Tuple
from spacy.tokens import Doc
from spacy.pipeline import Pipe
from spacy.language import Language
from spacy.lang.en import English
from typing import Optional
from dataclasses import dataclass

# normalize whitespace - multiple whitespace chars reduced to single
# e.g. "This  is a\n  test" => "this is a test"
def normalize_whitespace(text: str, preserve_line_breaks: bool=True) -> str:
    if preserve_line_breaks: # normalize only spaces, not line or paragraph breaks
        return regex.sub(pattern=r"\p{Separator}+", repl=" ", string=text).strip()
        # check if any better or worse (no Unicode entities so more generalizable)
        #return regex.sub(pattern=r"[^\S\r\n]+", repl=" ", string=text).strip()
    else:
        return " ".join(text.split())
    

@dataclass(frozen=True)
class Substitution:
    find: str|regex.Pattern
    repl: str
    ignoreCase: Optional[bool] = True


# text substitutions 
substitutions = {
    "en": {
        "spelling": [
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
        ],
        "ligature": [
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
        ],
        "punctuation": [
            # any dash character (where not followed by a number e.g. negative numbers) 
            # converted to a single standard hyphen, prefixed and suffixed with a space 
            Substitution(r"\b\s*(\p{Dash_Punctuation})\s*(?=[^\p{Number}])", " - "),
            Substitution(r"\b(\p{Dash_Punctuation})\b", " - "),
            # adding consistent spacing before/after slashes
            Substitution(r"\b\s*([\\\/])\s*\b", r" \1 "),
            # adding consistent spacing before/after brackets
            Substitution(r"([^\s])\s*(\p{Open_Punctuation})\s*([^\s])", r"\1 \2\3"),
            Substitution(r"([^\s])\s*(\p{Close_Punctuation})\s*([^\s])", r"\1\2 \3"),        
            # converting ampersand character (&) to "and"
            Substitution(r"(\p{Letter})\s+&\s+(\p{Letter})", r"\1 and \2"),
            # removing apostrophes
            Substitution(r"(\p{Letter})'s\s(\p{Letter})", r"\1s \2"),        
            Substitution(r"(\p{Letter}s)'\s(\p{Letter})", r"\1 \2"),
            # adding consistent spacing after commas
            Substitution(r"(\p{Letter}),(\p{Letter})", r"\1, \2")
        ],
        "whitespace": [
            # words hyphenated at line break - remove both hyphen and newline character
            # (typical pattern observed in text extracted from PDF docs, frustrates NER/IE)
            Substitution(r"(\p{Letter})\p{Separator}*[\r\n]([a-z])", r"\1 \2"),
            # remove hyphen at end of line
            Substitution(r"\p{Dash_Punctuation}\p{Separator}*[\r\n]([a-z])", r"\1"),
            # remove newline characters unless at end of a sentence
            Substitution(r"([^.])\p{Separator}*[\r\n]", r"\1 "),
            # convert multi-whitespace to single space (but preserving line-breaks)
            Substitution(r"\p{Separator}+", " ")
        ]
    }
}

def build_substitutions(
    lang: str, 
    normalize_spelling: bool=True,
    normalize_ligatures: bool=True, 
    normalize_whitespace: bool=True,         
    normalize_punctuation: bool=True 
    ) -> list[Substitution]:
    # create composite list of sustitutions based on options supplied. 
    # Order matters; add substitutions in order they should be applied
    # so normalize whitespace, ligatures & punctuation before spelling
    # then redo whitespace normalisation at end, after others have run  
    subs = []
    if normalize_whitespace: subs.extend(substitutions.get(lang, {}).get("whitespace", []))
    if normalize_ligatures: subs.extend(substitutions.get(lang, {}).get("ligature", []))
    if normalize_punctuation: subs.extend(substitutions.get(lang, {}).get("punctuation", []))
    if normalize_spelling: subs.extend(substitutions.get(lang, {}).get("spelling", []))
    # redo whitespace normalisation at end after others have run
    if normalize_whitespace: subs.extend(substitutions.get(lang, {}).get("whitespace", []))
    
    return subs
        

# spaCy pipeline class to perform the text normalisation using substitutions
class TextNormalizer(Pipe):    

    @staticmethod
    def _compileSub(sub: Substitution) -> Substitution:
        flags = regex.IGNORECASE | regex.MULTILINE if sub.ignoreCase else regex.MULTILINE
        return Substitution(regex.compile(pattern=sub.find, flags=flags), sub.repl, sub.ignoreCase)        

    def _normalize_text(self, text: str) -> str:
        # (optionally) decode unicode characters to ASCII equivalents (e.g. accents removed)
        # this can help with subsequent NER/IE, but may not be appropriate for all use cases
        text = unidecode(text) if self.decode_unicode else text
        
        # perform text replacement or regex replacement
        # (as appropriate) for each of the substitutions
        for item in self.substitutions:
            if isinstance(item.find, str):
                text = text.replace(item.find, item.repl)
            elif isinstance(item.find, regex.Pattern):  
                text = item.find.sub(item.repl, text)

        return text

    
    def __init__(self, nlp: Language, subs: list[Substitution] | None = None, decode_unicode: bool = True) -> None:
        self.nlp: Language = nlp
        self.decode_unicode: bool = decode_unicode
        # regex substitutions are compiled for subsequent (possibly repeated) use in the __call__ method
        self.substitutions: list[Substitution] = list(map(self._compileSub, subs)) if subs is not None else []

    def __call__(self, doc: Doc) -> Doc:
        # use substitutions to normalise the text of the Doc
        text = self._normalize_text(doc.text)

        # if nothing has changed, just return original doc
        # (to avoid performing unnecessary retokenization)
        if text == doc.text: return doc
                       
        # disable pipeline components to prevent running after retokenization
        disabled = self.nlp.select_pipes(disable=["ner", "text_normalizer"])
        # newDoc = self.nlp.make_doc(text) # note: make_doc doesn't do lemmas or pos, only tokenisation
        
        # retokenize the cleaned text  
        newDoc = self.nlp(text) 

        # ensure any doc-level extensions are carried over to the new doc       
        for ext_name, value in doc._.__dict__.items():
            if not ext_name.startswith("_"):
                setattr(newDoc._, ext_name, value)

        # ensure any token-level extensions are carried over to the new doc
        for old_token, new_token in zip(doc, newDoc):
            for ext_name, value in old_token._.__dict__.items():
                if not ext_name.startswith("_"):
                    setattr(new_token._, ext_name, value)

        # ensure any user data is carried over to the new doc        
        newDoc.user_data = doc.user_data.copy()    

         # re-enable any disabled components and return the new doc
        disabled.restore()
        return newDoc 
                

@Language.factory(
    name="text_normalizer", 
    default_config={ 
        "decode_unicode": True, 
        "substitutions": [] 
}) 
def create_text_normalizer(
    nlp: Language, 
    name: str = "text_normalizer",
    decode_unicode: bool = True,
    substitutions: list[Substitution] | None = None
    ) -> Pipe: 

    # create the TextNormalizer pipe with the substitutions        
    return TextNormalizer(
        nlp=nlp, 
        subs=substitutions, 
        decode_unicode=decode_unicode
    )


@English.factory(
    name="text_normalizer", 
    default_config={ "decode_unicode": True }
)
def create_text_normalizer_en(
    nlp: Language, 
    name: str = "text_normalizer", 
    decode_unicode: bool = True,
    ) -> Pipe:
    # create composite list of sustitutions to be applied to the text 
    subs: list[Substitution] = build_substitutions("en")
    return create_text_normalizer(
        nlp=nlp, 
        name=name, 
        decode_unicode=decode_unicode, 
        substitutions=subs
    )


# to test this module independently, run from package root:
# $ python -m components.TextNormalizer
if __name__ == "__main__":   
    import spacy    

    # create spaCy pipeline with text normalizer as first component, and NER disabled 
    nlp = spacy.load("en_core_web_sm", disable=["ner"]) 
    nlp.add_pipe("text_normalizer", first=True)

    # usage example - testing on text with inconsistent whitespace, punctuation and spelling 
    text = f"archeological  work in Bełżec indi-\ncated   an Iron Age/ Romano- British  /Roman\npost -hole, in( low -lying)ground.\nThis  was  near(vandal-\nized)\n  mediæval/post-medieval(15th-17th century? )foot-\nings. Items of Mediaeval &  paleolithic(archeological)jewelry dated to the 2nd -  3rd century and pottery & vertebræ of a fœtus were  located in the New Harbor area.  Gray colored  & oxidized,aluminum artifacts were   found near the theater."
           
    print(f"\nBefore:\n\"{text}\"")
    doc = nlp(text)
    print(f"\nAfter:\n\"{doc.text}\"")   
    