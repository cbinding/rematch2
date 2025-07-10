"""
=============================================================================
Package :   rematch2
Module  :   BaseRuler.py
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy custom pipeline component (specialized SpanRuler)
            base class for other custom ruler pipeline components
Imports :   Doc, SpanRuler, Language, functools, time
Example :       
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History :   
02/07/2025 CFB was 'CustomSpanRuler', All other rulers now based on this
                (mainly so we can time function calls for performance)
=============================================================================
"""
from spacy.tokens import Doc
from spacy.pipeline import SpanRuler
from spacy.language import Language
import functools
import time
from .Decorators import run_timed

class BaseRuler(SpanRuler):
    
    #@run_timed
    def __call__(self, doc: Doc) -> Doc:
        print(f"{self.name}")
        return SpanRuler.__call__(self, doc)      


    # normalize input patterns - used for consistency in custom rulers
    # patterns: [{id: "", label: "", pattern: []}, {id, label, pattern: []},...]    
    @staticmethod
    def normalize_patterns(
        nlp: Language, 
        patterns: list=[],
        default_label: str="UNKNOWN",
        lemmatize: bool=True,
        min_lemmatize_length: int=4,
        min_term_length: int=3,
        pos: list[str]=[]
        ) -> list:

        normalized_patterns = []

        for item in patterns:
            # clean passed in values before using
            clean_id = item.get("id", "").strip()
            clean_label = item.get("label", default_label).strip()

            # any pos already present in the pattern overrides passed arg
            clean_pos = item.get("pos", pos)             

            # is a pattern present? (may be either a list or a string)
            pattern = item.get("pattern", "")
            if len(pattern) > 0:

                # if already a pre-structured token pattern [{}, {}, ...]
                if isinstance(pattern, list):

                    # just append to normalized_patterns as is
                    normalized_patterns.append({
                        "id": clean_id,
                        "label": clean_label,
                        "pattern":  pattern
                    })

                # if it is a string term or phrase
                elif isinstance(pattern, str):
                        
                    # NOTE - main text normalisation is now part of the pipeline
                    # so is handled below in doc = nlp.make_doc(clean_phrase)
                    clean_phrase = pattern.lower()          
                    
                    # if too small don't include it at all
                    if len(clean_phrase) < min_term_length:
                        continue

                    # first tokenize the phrase
                    doc = nlp.make_doc(clean_phrase)
                    phrase_length = len(doc)
                        
                    # build a new token pattern for this phrase
                    new_pattern = []                    
                    # for each term (token) in the phrase
                    # for n, tok in enumerate(doc, 0):
                    for tok in doc:
                        element = {}

                        # lemmatize term if required (and if term long enough). Uses both lemma AND original term,
                        # lemmatization may not work on capitalised text (as spaCy may regard it as a proper noun),
                        # and there doesn't seem a way to specify a rule to match on the lowercase of the lemma                    
                        text = (tok.text or "").strip()
                        
                        if (lemmatize == True and len(text) >= min_lemmatize_length):
                            # lemmatization of full text may be different to lemmatisation of vocabulary term,
                            # and cannot use "LOWER" in conjunction with "LEMMA" in spaCy patterns here, so  
                            # using a set to list unique case variants of either original term text OR lemma 
                            # so pattern built here is:
                            # [
                            # { "LEMMA": { "IN" { [ "SKIRT", "skirt", "Skirt", "SKIRTING", "skirting", "Skirting" ]}}},
                            # { "LEMMA": { "IN" { [ "BOARD", "board", "Board", "BOARDS", "boards", "Boards" ]}}}
                            # ] 
                            lemma = (tok.lemma_ or "").strip()
                        
                            variants = {
                                lemma.upper(), 
                                lemma.lower(), 
                                lemma.title(), 
                                text.upper(), 
                                text.lower(), 
                                text.title()
                            }                        
                            
                            element["LEMMA"] = { "IN": list(variants) }   
                        else:
                            # just match the term, ignore case. Pattern built here is:
                            # [{ "LOWER": "skirting" }, { "LOWER": "boards" }]   
                            element["LOWER"] = text.lower()                       
                        
                        # add POS restriction if any passed in or any present in this item
                        # note 06/03/2024 - POS (was) only applied to LAST term if multi-word phrase
                        # e.g. { "LEMMA": "board", "POS": { "IN": ["NOUN", "PROPN"] }}
                        # POS now applied ONLY to single terms, NOT to multi-word phrases, which
                        # are regarded more likely to be correct matches without POS restriction
                        if (len(clean_pos) > 0 and phrase_length == 1):
                            if isinstance(clean_pos, list):
                                element["POS"] = { "IN": clean_pos }
                            elif isinstance(clean_pos, str):
                                element["POS"] = { "IN": [clean_pos] }

                        new_pattern.append(element)
                        
                    # add newly built pattern to normalized_patterns
                    # print(new_pattern)
                    normalized_patterns.append({
                        "id": clean_id,
                        "label": clean_label,
                        "pattern":  new_pattern
                    })

        # finally, return the normalized list        
        return normalized_patterns
    