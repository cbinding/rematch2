from spacy.language import Language

# normalize string whitespace
def normalize_whitespace(s: str = ""): 
    return ' '.join(s.strip().split()) 


# normalize input patterns for use with custom rulers
# patterns: [{id, label, pattern}, {id, label, pattern},...]    
def normalize_patterns(
    nlp: Language, 
    patterns: list=[],
    default_label: str="UNKNOWN",
    lemmatize: bool=True,
    min_lemmatize_length: int=4,
    min_term_length: int=3,
    pos: list=[]
    ) -> list:
    normalized_patterns = []

    for item in patterns:
        # clean values before using
        clean_id = normalize_whitespace(item.get("id", ""))
        clean_label = normalize_whitespace(item.get("label", default_label))
        pattern = item.get("pattern", "")

        # is there even a pattern present? 
        # (at this point it may be a list or a str)
        if len(pattern) > 0:

            # if already a token pattern  [{},{}]
            if isinstance(pattern, list):

                # just add to normalized_patterns
                normalized_patterns.append({
                    "id": clean_id,
                    "label": clean_label,
                    "pattern":  pattern
                })

            # if phrase pattern (plain string term/phrase)   
            elif isinstance(pattern, str):
                    
                # normalize whitespace (inconsistent whitespace can frustrate matching)
                clean_phrase = normalize_whitespace(pattern)
                    
                # if too small don't include it at all
                if len(clean_phrase) < min_term_length:
                    continue

                # first tokenize the phrase
                doc = nlp(clean_phrase)
                phrase_length = len(doc)
                    
                # build a new token pattern for this phrase
                new_pattern = []                    
                # for each term (token) in the phrase
                for n, tok in enumerate(doc, 1):
                    element = {}

                    # lemmatize term if required (providing term is long enough)
                    # e.g. "skirting boards":
                    # { "LEMMA": "skirt" }, { "LEMMA": "board" } or
                    # { "LOWER": "skirt" }, { "LOWER": "board" }
                    # IMPORTANT: lemmatization doesn't work if the text is
                    # capitalised as spaCy mistakes it for a proper Noun
                    if (lemmatize and len(tok.text) >= min_lemmatize_length):
                        element["LEMMA"] = tok.lemma_.lower()
                    else:
                        element["LOWER"] = tok.text.lower()  
                    
                    # add pos tags check if any passed in
                    # note POS only applied to LAST term if multi-word phrase
                    # e.g. { "LEMMA": "board", "POS": { "IN": ["NOUN", "PROPN"] }}
                    if (len(pos) > 0 and n == phrase_length):
                        element["POS"] = {"IN": pos}

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


def _patterns_from_json_file(file_path: str) -> list:
    patterns = []

    with open(file_path, "r") as f:
        patterns = json.load(f)

    return patterns

