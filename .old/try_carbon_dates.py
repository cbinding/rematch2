# test sentence splitting approaches
import spacy # for sentence splitter
from spacy.lang.en import English 
from spacy.matcher import DependencyMatcher
from spacy.matcher import Matcher

input_text = "The find was initially radiocarbon dated to 2,500 cal BP but possibly radiocarbon date 300 BC ± 75 years. It was definitely not as early as radiocarbon year 3000 cal BP."

nlp = spacy.load("en_core_web_sm", disable=["ner"])
doc = nlp(input_text)
#spacy.displacy.serve(doc, style="dep")

# https://en.wikipedia.org/wiki/Radiocarbon_dating
# Calibrated C14 dates: "cal BP", "cal BC", "cal AD", with 'BP' referring to the year 1950 as the zero date
# (note BP for radiocarbon dates present is usually 1950, but in thermoluminescence dating it is 1980)
# dates include associated probable error or standard deviation, e.g. "2500 cal BP ± 30 years"
# uncalibrated dates: "lab: C14year ± range BP" e.g. "UtC-2020: 3510 ± 60 BP" (but sometimes no whitespace or lab: "3510±60BP")
# "2.3 ka BP" means 2,300 radiocarbon years before present (present being 1950) - i.e. 350 BC

pattern = [
    {  
        "RIGHT_ID": "year_suffix",
        "RIGHT_ATTRS": {"LOWER": {"REGEX": r"^b\.?[cp]\.?$"}}
    },
    {   
        "LEFT_ID": "year_suffix",
        "RIGHT_ID": "cal_indicator",
        "REL_OP": ";",
        "RIGHT_ATTRS": {"DEP": "compound", "LOWER": {"REGEX": r"^cal\.?$"}}       
    },
    {   
        "LEFT_ID": "cal_indicator",
        "RIGHT_ID": "year_value",
        "REL_OP": ";",
        "RIGHT_ATTRS": {"DEP": "nummod", "LIKE_NUM": True}
    },
    {   
        "LEFT_ID": "year_value",
        "RIGHT_ID": "radiocarbon_indicator",
        "REL_OP": ";*",
        "RIGHT_ATTRS": {"LOWER": "radiocarbon"}
    }
]


matcher = DependencyMatcher(vocab=nlp.vocab, validate=True)
matcher.add("RADIOCARBON_DATE", [pattern])
matches = matcher(doc)
#print(matches)

for match_id, token_ids in matches:
    print(f"Matched Tokens: {[doc[i].text for i in token_ids]}")

# not using dependency matcher, just proximity
pattern = [
    {"LOWER": "radiocarbon"},
    {"OP": "?", "IS_ALPHA": True},
    {"OP": "?", "IS_ALPHA": True},
    {"LIKE_NUM": True},
    {"OP": "*", "LOWER": {"REGEX": r"^cal\.?$"}},
    {"LOWER": {"REGEX": r"^b\.?[cp]\.?$"}}
]
matcher = Matcher(nlp.vocab)
matcher.add("RADIOCARBON_DATE", [pattern])
matches = matcher(doc)
#print(matches)
for match_id, start, end in matches:
    string_id = nlp.vocab.strings[match_id]  # Get string representation
    span = doc[start:end]  # The matched span
    print(match_id, string_id, start, end, span.text)
   