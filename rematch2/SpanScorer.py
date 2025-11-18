# add weighting and scores to spans
import spacy, os
from spacy.tokens import Doc, Span
from spacy.pipeline import Pipe
from spacy.matcher import Matcher
from spacy.language import Language
from spacy.vocab import Vocab
from .Util import DEFAULT_SPANS_KEY
from .SpanRelationship import *
from collections import Counter
import pandas as pd
from pandas import DataFrame
from rematch2.DocSummary import DocSummary


class BaseMatcher(Matcher):
    def __init__(self, vocab: Vocab, validate: bool=True):
        super().__init__(vocab, validate=validate)        
        
    # Add single word (case-insensitive) pattern for each term in terms
    # TODO: could normalize these?
    def add_terms(self, label: str="unknown", terms: list[str]=[]) -> None:
        patterns = [[{"LOWER": term.lower()}] for term in terms]
        self.add_patterns(label, patterns)

    # Add patterns passed in (see spaCy matcher pattern syntax)
    def add_patterns(self, label: str="unknown", patterns: list=[]) -> None:
        self.add(label, patterns)

    # return a list of spans matching the terms or patterns passed in
    def __call__(self, doc: Doc) -> list[Span]:
        matches = super().__call__(doc, as_spans=True)
        # remove duplicates and overlaps, keep longest
        matches = spacy.util.filter_spans(matches) 
        return matches
    

class SignificanceMatcher(BaseMatcher):
    def __init__(self, vocab: Vocab, validate: bool=True):
        super().__init__(vocab, validate=validate)
        terms = [
            "significant",
            "significance", 
            "substantial", 
            "important", 
            "importantly",
            "importance",
            "major", 
            "considerable", 
            "compelling", 
            "notable", 
            "noteworthy",
            "pertinent",
            "dendro", 
            "dendrochonology",
            "dendrochonological",
            "calibrated",
            "calibration",
            "radiocarbon",
            "carbon", 
            "carbon14", 
            "C14"
        ]
        patterns = [
            [{"LOWER": "radio"}, {"OP": "?", "ORTH": "-"}, {"LOWER": "carbon"}, {"OP": "?", "LOWER": {"REGEX": "dat(ing|ed|e)"}}],
            [{"LOWER": "most"}, {"LOWER": {"REGEX": "important(ly)?"}}],
            [{"LOWER": {"REGEX": "strong(er)?"}}, {"LOWER": "evidence"}, {"OP": "?", "LOWER": {"REGEX": "(for|of)"}}],
            [{"LOWER": "carbon"}, {"LOWER": {"REGEX": "dat(s|e|ing|ed)"}}],
            [{"LOWER": "rare"}, {"LOWER": "example"},{"OP": "?", "LOWER": "of"}]
        ]
        super().add_terms("significance", terms)
        super().add_patterns("significance", patterns)
                

class NegationMatcher(BaseMatcher):
    def __init__(self, vocab: Vocab, validate: bool=True):
        super().__init__(vocab, validate=validate)
        terms = ["preclude", "precluded", "precludes", "precluding"]
        patterns = [
            [{"LOWER":  {"REGEX": "^(lack|scarcity|absence)$"}}, {"LOWER": "of"}],
            [{"LOWER": {"REGEX": "^(no|lack(s|ed))$"}},{"LOWER": "evidence"}, {"OP": "?", "LOWER": "of"}],
            [{"LOWER": "did"}, {"LOWER": "not"}, {"LOWER": "indicate"}],
            [{"LOWER": "lack"}, {"LOWER": "of"}, {"OP": "?", "LOWER": "evidence"}],
            [{"LOWER": "not"}, {"LOWER":  {"REGEX": "(suggest(ed)?|reveal(ed)?|detected)"}}],
            [{"LOWER": {"REGEX": "fail(s|ed)"}}, {"LOWER": "to"}, {"LOWER": "reveal"}],
            [{"LOWER": {"REGEX": "(is|was)"}}, {"LOWER": "absent"}]
        ]
        super().add_terms("negation", terms)
        super().add_patterns("negation", patterns)


class SpanScorer(Pipe):
        
    def __init__(self, 
        nlp: Language, 
        spans_key: str = DEFAULT_SPANS_KEY, 
        #max_proximity: int = 3, 
        #significance_weight: float = 1.0, 
        #significance_terms: list = []
         ) -> None:

        self.nlp: Language = nlp
        self.spans_key: str = spans_key.strip()
        #self.max_proximity: int = max_proximity
        #self.significance_weight: float = significance_weight
        #self.significance_terms: list = list(map(lambda s: s.strip().lower(), significance_terms))
        

    # multiple metrics to run
    def __call__(self, doc: Doc) -> Doc:
        doc = self.set_section_scores(doc)
        doc = self.set_negation_scores(doc)
        doc = self.set_frequency_scores(doc)
        doc = self.set_significance_scores(doc)
        return doc 


    # scoring for the section the span occurs within (unfinished)
    def set_section_scores(self, doc: Doc) -> Doc:
         # ensure the custom properties exist before use
        if not Span.has_extension("sec_score"):
            Span.set_extension("sec_score", default=0.0)
        return doc


    # scoring for frequency of occurrence of the concept
    def set_frequency_scores(self, doc: Doc) -> Doc:
        # ensure that custom properties exist before use
        if not Span.has_extension("occurrences"):
            Span.set_extension("occurrences", default=0)   

        if not Span.has_extension("frequency"):
            Span.set_extension("frequency", default=0.0)

        if not Span.has_extension("frequency_explain"):
            Span.set_extension("frequency_explain", default="")
        
        # get all the current spans
        all_spans = list(doc.spans.get(self.spans_key, []))
        if len(all_spans) < 1: return doc

        # count occurrences by id (or text if no id) and by label
        ident_count = Counter(map(lambda s: s.text.lower() if not s.id else s.id, all_spans))
        label_count = Counter(map(lambda s: s.label, all_spans))
        
        # set scores on each span
        for span in all_spans:
            id: str = span.text.lower() if not span.id else span.id
            lbl: str = span.label
            id_count: int = ident_count.get(id, 0) 
            lbl_count: int = label_count.get(lbl, 1) # avoid divide by zero
            span._.occurrences = id_count
            span._.frequency = float(id_count) / float(lbl_count)
            span._.frequency_explain = f"id_count={id_count}, lbl_count={lbl_count}"
        return doc
    

    # get textual context around a span
    @staticmethod
    def get_span_context(span: Span, window_size: int=4) -> str:
        doc = span.doc
        start = max(span.start - window_size, 0)
        end = min(span.end + window_size, len(doc))
        context_span = doc[start:end]
        return context_span.text


    # scoring for proximity to a 'significant' term or phrase
    def set_significance_scores(self, doc: Doc) -> Doc:
        matcher = SignificanceMatcher(doc.vocab)        
        matches = matcher(doc)      
        self.set_proximity_scores(doc, matches, max_proximity=3, property_name="sig_score", property_score=1.0)
        return doc
    

    # scoring for proximity to a 'negation' term or phrase
    def set_negation_scores(self, doc: Doc) -> Doc:
        matcher = NegationMatcher(doc.vocab)        
        matches = matcher(doc)
        self.set_proximity_scores(doc, matches, max_proximity=3, property_name="neg_score", property_score=1.0)
        return doc


    def set_proximity_scores(
        self, 
        doc: Doc, 
        proximity_to: list[Span], 
        max_proximity: int=4, 
        property_name: str="score", 
        property_score: float=0.0) -> Doc:

        # ensure the named custom property exists before use 
        clean_property_name = property_name.strip().lower()
        if not Span.has_extension(clean_property_name):
            Span.set_extension(clean_property_name, default=0.0)

        # get all the current spans
        all_spans = list(doc.spans.get(self.spans_key, []))
        if len(all_spans) == 0: return doc

        # For each span, compute min token distance to any 'proximity_to' span (in the same sentence)
        for span in all_spans:
            nearby = list(filter(lambda s: s.sent == span.sent, proximity_to))
            if(len(nearby) == 0): continue

            min_distance = min(
                (near.start - (span.end - 1)) if span_before(span, near) or span_meets(span, near) else
                (span.start - (near.end - 1)) if span_after(span, near) or span_met_by(span, near) else 0
                for near in nearby
            )   
            if min_distance <= max_proximity:
                setattr(span._, clean_property_name, property_score)
                #span._[clean_property_name] = property_value # syntax doesnt work

        return doc 
    

@Language.factory(name="span_scorer", default_config={"spans_key": DEFAULT_SPANS_KEY}) 
def create_span_scorer(
    nlp: Language, 
    name: str="span_scorer", 
    spans_key: str=DEFAULT_SPANS_KEY) -> Pipe:
    return SpanScorer(nlp, spans_key=spans_key)


# test the span_scorer pipeline component
if __name__ == "__main__":
    import spacy

    # TODO: get PDF files from URL, integrate mark's PDF to text script everywhere (cache the text),
    BASE_PATH = "./data/oasis/journals_july_2024/text extraction - new/"

    # build the pipeline
    nlp = spacy.load("en_core_web_sm", disable=["ner"]) 
    nlp.add_pipe("normalize_text", before = "tagger")
    nlp.add_pipe("yearspan_ruler", last=True)
    nlp.add_pipe("periodo_ruler", last=True, config={"periodo_authority_id": "p0kh9ds"}) 
    nlp.add_pipe("fish_archobjects_ruler", last=True)
    nlp.add_pipe("child_span_remover", last=True) 
    nlp.add_pipe("span_scorer", last=True)
    # note could also call it after main pipeline runs, like this:
    # scorer = SpanScorer(nlp)
    # doc = scorer(doc)

    file_names = [
        "surreyac103_063-090_lambert_new.txt",
        "2022_96_013-068_Huxley_new.txt",
        "surreyac103_307-321_nelson_new.txt",
        "surreyac103_091-172_haslam_new.txt"
    ]

    for file_name in file_names:
        file_path = os.path.join(BASE_PATH, file_name)        
        print(f"reading \"{file_path}\"")
        with open(file_path, "r") as f:
            input_text = f.read()
        
        # run the pipeline on the text and get all identified spans
        print(f"processing text through pipeline")
        doc = nlp(input_text)
        
        matcher = SignificanceMatcher(nlp.vocab)    
        sig_spans = matcher(doc)
        print("Significance spans:")
        for span in sig_spans:
            print(f"[{span.start}:{span.end -1}] {span.text}")

        matcher = NegationMatcher(nlp.vocab)    
        neg_spans = matcher(doc)
        print("Negation spans:")
        for span in neg_spans:
            print(f"[{span.start}:{span.end - 1}] {span.text}")
        
        # output the results        
        summary = DocSummary(doc)
        output_file_name = os.path.join(BASE_PATH, f"span_scoring_output_{file_name}.csv")
        print("Writing output to ", output_file_name)
        with open(output_file_name, "w") as f:
            summary.spans_to_csv(file=f)
