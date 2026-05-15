import spacy
from spacy.matcher import Matcher
from spacy.lang.en import English 
from spacy.pipeline import SpanRuler

text = "It was constructed around 1500 BCE, ruined approximately 400 B.C. and discovered circa 1700 A.D."

# trying better way to specify modular patterns for matching yearspan phrases...
prefixes = [{"LOWER": {"REGEX": {"IN": [r"^c\.$", "circa", "around", "approximately"]}}}]
yearspan = [{"LOWER": {"REGEX": r"^\d{3,4}$"}}]
suffixes = [{"LOWER": {"REGEX": {"IN": [r"^b\.?c\.?(e\.?)?", r"a\.?d\.?", r"c\.?e\.?"]}}}]
combined = prefixes + yearspan + suffixes
matcher = Matcher(nlp.vocab)
matcher.add("COMBINED", [combined])

nlp = English()
doc = nlp(text)
matches = matcher(doc)
for match_id, start, end in matches:
    print(f"Matched: \"{doc[start:end].text}\"")
# Matched: around 1500 BCE
# Matched: approximately 400 B.C.
# Matched: circa 1700 A.D.

# now using SpanRuler (or is approach above good enough??)
prefix_patterns = [r"^c\.$", "circa", "around", "approximately"]
suffix_patterns = [r"^A\.?D.\?$", r"^C\.?E.\?$", r"B\.?C\.?(E\.?)?"]
#TODO - continue this...  
#datesuffix_patterns = list(map(lambda p: p["pattern"], patterns_en_DATESUFFIX))
#pattern = "{ LOWER: "}"
   
ruler = nlp.add_pipe("span_ruler")
ruler.add_patterns(combined)

doc = nlp(text)
self._doc.spans.get(self._spans_key, [])


