r"""
=============================================================================
Package   : rematch2
Module    : StringCleaning.py
Classes   : 
Project   : ATRIUM
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : 
    ***** NOTE - deprecated, this code now implemented as custom pipeline components
    see TextNormalizer.py *****
    Functions for performing string cleaning and normalisation operations on 
    text, prior to any information extraction work. Mostly based on regex replacement patterns. 
    Functions allow chaining and pipelining: f(text: str) -> str
    NOTE: using 'regex' library not 're' - to support Unicode category groups 
    e.g. r"\p{Dash_Punctuation}" (represents any hyphenation character)
    for list of unicode categories see https://www.regular-expressions.info/unicode.html
    TODO (possibly): normalize_case, normalize_diacritics, normalize_contractions
    # (wasn't, couldn't i'm etc.) - probably rare but note how they get tokenized - see
    https://theslaps.medium.com/cant-stand-don-t-want-contractions-with-spacy-39715cac2ebb
Imports   : regex, spacy (for testing tokenization only)
Example   : clean = normalize_text(text)
License   : https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History
05/08/2024 CFB Initially created script
=============================================================================
"""
import regex
from regex import Match
    
# normalize whitespace - multiple whitespace chars reduced to single
# e.g. "This  is a\n  test" => "this is a test"
def normalize_whitespace(text: str, preserve_line_breaks: bool=True) -> str:
    if preserve_line_breaks: # normalize only spaces, not line or paragraph breaks
        return regex.sub(pattern=r"\p{Separator}+", repl=" ", string=text).strip()
        # check if any better or worse (no Unicode entities so more generalizable)
        #return regex.sub(pattern=r"[^\S\r\n]+", repl=" ", string=text).strip()
    else:
        return " ".join(text.split())
    
# sometimes normally single words hyphenated at line break;
# in this case remove both the hyphen and newline character
# e.g. "...the para-
# "graph concludes with..." => "...the paragraph concludes with..."
def remove_newline_hyphens(text: str) -> str:
    return regex.sub(pattern=r"\p{Dash_Punctuation}\p{Separator}*[\r\n]([a-z])", repl=r"\1", string=text).strip()

# sometimes newlines present to maintain line width.
# retain if at the end of a sentence, otherwise
# can be removed without altering sentence meaning 
def remove_spurious_newlines(text: str) -> str:
     return regex.sub(pattern=r"([^.])\p{Separator}*[\r\n]", repl=r"\1 ", string=text).strip()


# normalise spelling (English only;  mainly US -> UK spelling)
# controlled entry vocabulary should include these variants
# but not guaranteed
def normalize_spelling(text: str) -> str:    
    subs = {
        "(a)rcheo": r"\1rchaeo",
        "(p)aleo": r"\1alaeo",
        r"\bdefense\b": "defence",
        r"\bpalestra\b": "palaestra",
        r"\b(m)ediaeval\b": r"\1edieval", # ignore case but retain in result
        r"(\w+)ization\b": r"\1isation",
        r"(\w+)izing\b": r"\1ising",
        r"(\w+)ized\b": r"\1ised",
        r"\bjewelry\b": "jewellery",
        r"\bartifact\b": "artefact",
        r"\bplow\b": "plough",
        r"sulfate\b": "sulphate",
        r"\bsulfur\b": "sulphur",
        r"theater\b": "theatre",
        r"\bmodeled\b": "modelled",
        r"\bmodeling\b": "modelling",
        r"\bharbor\b": "harbour",
        r"\blabor\b": "labour",
        r"\baluminum\b": "aluminium",
    }

    result = text
    for key, val in subs.items():
        result = regex.sub(pattern=key, repl=val, string=result, flags=regex.IGNORECASE | regex.MULTILINE)

    return result


# normalize spacing on any dash/hyphen punctuation character
# this makes subsequent tokenisation more consistent
# so rule-based patterns can match properly
# e.g. "post- hole" | "post -hole" | "post-hole" | "post - hole" => "post - hole" 
# e.g. "10th-13th century" => "10th - 13th century"
# e.g. "dating from -500" => "dating from -500"  (unaffected)
def normalize_hyphens(text: str) -> str:
    result = text
    result = regex.sub(pattern=r"\b\s*(\p{Dash_Punctuation})\s*(?=[^\p{Number}])", repl=r" - ", string=result)
    result = regex.sub(pattern=r"\b(\p{Dash_Punctuation})\b", repl=r" - ", string=result)
    return result


# normalize spacing of forward and back slashes
# e.g. "Georgian/Victorian" => "Georgian / Victoria"
# e.g. "Georgian \Victorian" => "Georgian \ Victoria"
# e.g. "Georgian/ Victorian" => "Georgian / Victoria"
def normalize_slashes(text: str) -> str:
    result = text
    result = regex.sub(pattern=r"\b\s*([\\\/])\s*\b", repl=r" \1 ", string=result)
    return result


# normalize spacing before open bracket and after close bracket
# e.g. "the(quick)brown fox" => "the (quick) brown fox"
def normalize_brackets(text: str) -> str:
    result = text
    # normalize spacing before and after open bracket character "{[("
    result = regex.sub(pattern=r"([^\s])\s*(\p{Open_Punctuation})\s*([^\s])", repl=r"\1 \2\3", string=result)
    # normalize spacing before and after close bracket character "}])"
    result = regex.sub(pattern=r"([^\s])\s*(\p{Close_Punctuation})\s*([^\s])", repl=r"\1\2 \3", string=result)
    return result

# this function adapted from https://pypdf.readthedocs.io/en/stable/user/post-processing-in-text-extraction.html
def normalize_ligatures(text: str) -> str:
    ligatures = {
        "ﬀ": "ff",
        "ﬁ": "fi",
        "ﬂ": "fl",
        "ﬃ": "ffi",
        "ﬄ": "ffl",
        "ﬅ": "ft",
        "ﬆ": "st",
        # "Ꜳ": "AA",
        # "Æ": "AE",
        "ꜳ": "aa",
    }
    result = text
    for search, replace in ligatures.items():
        result = text.replace(search, replace)
    return result


# convert ampersands to "and"
def normalize_ampersands(text: str) -> str:
    result = text
    result = regex.sub(pattern=r"(\p{Letter})\s+&\s+(\p{Letter})", repl=r"\1 and \2", string=result)
    return result


# normalize apostrophes by eliminating them:
# remove from "architect's plans" or "archaeologists' tools"
# (but not from contractions e.g. "can't", "won't" etc.)
def normalize_apostrophes(text: str) -> str:
    result = text
    result = regex.sub(pattern=r"(\p{Letter})'s\s(\p{Letter})", repl=r"\1s \2", string=result)
    result = regex.sub(pattern=r"(\p{Letter}s)'\s(\p{Letter})", repl=r"\1 \2", string=result)
    return result


# remove bracketed suffixes (usually from vocabulary terms)
# e.g. "Visual Buildings Record (Level 1)" => "Visual Buildings Record"
# e.g. "Weapons <by form>" => "Weapons"
# Note not necessarily a good idea, it can produce multiple ambiguous matches
def remove_bracketed_suffix(text: str) -> str:   
    result = text
    result = regex.sub(r"\s\<[^\>]+\>$", "", result) # remove angle bracketed suffix
    result = regex.sub(r"\s\([^\)]+\)$", "", result) # remove curve bracketed suffix
    #result = re.sub(r"\s\p{Ps}[^\p{Pe}]+\p{Pe})$", "", result) # remove ANY bracketed suffix
    return result


def selection_upper_case(text: str, pattern: str=r".*", count: int=0, flags=None) -> str:
    #default_config = { pattern: r".*", count: 0, flags: None }
    #merged_config = default_config | config
    def repl(match: Match) -> str: return match[0].upper()
    if flags is not None:
        return regex.sub(pattern=pattern, repl=repl, string=text, count=count, flags=flags)
    else:
        return regex.sub(pattern=pattern, repl=repl, string=text, count=count)


def selection_lower_case(text: str, pattern: str=r".*", count: int=0, flags=None) -> str:
    def repl(match: Match) -> str: return match[0].lower()
    if flags is not None:
        return regex.sub(pattern=pattern, repl=repl, string=text, count=count, flags=flags)
    else:
        return regex.sub(pattern=pattern, repl=repl, string=text, count=count)


def selection_snake_case(text: str, pattern: str=r".*", count: int=0, flags=None) -> str:
    def repl(match: Match) -> str: return regex.sub(r"\s+", "_", match[0].lower()) 
    if flags is not None:
        return regex.sub(pattern=pattern, repl=repl, string=text, count=count, flags=flags)
    else:
        return regex.sub(pattern=pattern, repl=repl, string=text, count=count)


# note this won't account for text already being eg snake case as it's only replacing spaces
def selection_kebab_case(text: str, pattern: str=r".*", count: int=0, flags=None) -> str:
    def repl(match: Match) -> str: return regex.sub(r"\s+", "-", match[0].lower())
    if flags is not None:
        return regex.sub(pattern=pattern, repl=repl, string=text, count=count, flags=flags)
    else:
        return regex.sub(pattern=pattern, repl=repl, string=text, count=count)


def selection_title_case(text: str, pattern: str=r".*", count: int=0, flags=None) -> str:
    def repl(match: Match) -> str: return match[0].title()
    if flags is not None:
        return regex.sub(pattern=pattern, repl=repl, string=text, count=count, flags=flags)
    else:
        return regex.sub(pattern=pattern, repl=repl, string=text, count=count)


def selection_sentence_case(text: str, pattern: str=r".*", count: int=0, flags=None) -> str:
    def repl(match: Match) -> str: return match[0].capitalize()
    if flags is not None:
        return regex.sub(pattern=pattern, repl=repl, string=text, count=count, flags=flags)
    else:
        return regex.sub(pattern=pattern, repl=repl, string=text, count=count)


#see https://dzone.com/articles/python-function-pipelines-streamlining-data-proces (sic)
# what if we want to pass options to functions?
def pipeline(*functions):
    
    def inner(data):
        result = data
        # Iterate functions
        for f in functions:
            result = f(result)
        return result
    return inner


# normalize text for information extraction
normalize_text = pipeline(
    remove_newline_hyphens, 
    remove_spurious_newlines,   
    normalize_whitespace,
    normalize_hyphens, 
    normalize_slashes, 
    normalize_brackets,
    normalize_spelling,
    normalize_ligatures,
    normalize_ampersands,
    normalize_apostrophes,
    normalize_whitespace,
    #remove_bracketed_suffix
)

r"""
Real examples (source: OASIS-descr-examples.xml)
hyphenation:
    * preconst3-158724 "mid- to late Iron Age"
    * molas1-63676 "1st- early 2nd century"
    * mas1-69918 "Mesolithic non- anthropogenic woodland"
    * archaeol7-38018 "18th -early 19th century"
spelling:
    * wessexar1-132784 "recorded archeologically"
    * chrisbut1-210291 "treethrow or paleochannel"
    * archaeol7-7178 "mediaeval settlements"
slashes:
    * preconst1-4915 "Mesolithic/ Early Neolithic" - fixed - MESOLITHIC NOW FOUND
    * wessexar1-125791 "Iron Age /Romano-British" - fixed - ROMANO-BRITISH NOW FOUND
    * molas1-284845 "Mesolithic\Neolithic" - fixed, NICE, BOTH NOT FOUND BEFORE
brackets:
    * molas1-11280 "Mesolithic(Holocene)" - fixed, NICE, BOTH NOT FOUND BEFORE
    * headland5-409537 "(ref 20/02046/PLF)for the"
    spaces:
    * preconst1-4915 "development.     Three residual"
    * cotswold2-237041 "There   were   numerous drainage ditches"
"""

# test the functions
if __name__ == "__main__":
    import spacy

    nlp = spacy.load("en_core_web_sm")
    text = f"archeological  work indi-\ncated  an Iron Age/ Romano- British  /Roman\npost -hole, in( low -lying)ground.\nThis  was  near(vandal-\nized)\n  Mediaeval/post-medieval(15th-17th century? )foot-\nings"
    text2 = f"clay pipes (smoking)"
    print(f"Old text:\n\"{text}\"")
    print(f"Old tokenization:")
    doc = nlp(text)
    print(list(map(lambda tok: tok.text, doc)))
    print(f"\n")
    clean = normalize_text(text)
    print(f"New text:\n\"{clean}\"")
    print(f"New tokenization:")
    doc = nlp(clean)
    print(list(map(lambda tok: tok.text, doc)))    