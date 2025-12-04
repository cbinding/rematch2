# add weighting and scores to spans
import spacy, os, json
from typing import Iterable, Any, cast
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


    def __call__(self, doc: Doc, *args, **kwargs) -> Any:
        # Ensure we always receive spans from the base Matcher by forcing as_spans=True.
        # Accept flexible args/kwargs to remain compatible with the base signature.
        kwargs["as_spans"] = True
        matches = super().__call__(doc, *args, **kwargs)
        # remove duplicates and overlaps, keep longest
        matches = spacy.util.filter_spans(cast(Iterable[Span], matches))
        return matches
    
    

class SignificanceMatcher(BaseMatcher):
    def __init__(self, vocab: Vocab, validate: bool=True):
        super().__init__(vocab, validate=validate)
        terms = [
            "C14",
            "calibrated",
            "calibration",
            "carbon", 
            "carbon14", 
            "compelling", 
            "conclusions",
            "considerable", 
            "crucial",
            "crucially",
            "demonstrates",
            "dendro", 
            "dendrochonological",
            "dendrochonology",
            "excellent",
            "exceptional",
            "exceptionally",
            "extraordinary",
            "extraordinarily",
            "importance",
            "importantly",
            "major", 
            "meaningful",
            "notable", 
            "notably",
            "noteworthy",
            "pertinent",
            "pivotal",
            "radiocarbon",
            "rare",
            "rarity",
            "relevant",
            "remarkable",
            "salient",
            "spectacular",
            "surprisingly",
            "understanding",
            "unexpectedly",
            "unique",
            "unusual",
            "valuable",
            "vital",
            "worthwhile",
            "significant",
        ]
        patterns = [
            [{"OP": "?", "LOWER": {"REGEX": "(quite|exceptionally|extraordinarily|particularly|highly|most|very|extremely|nationally)"}},  {"LOWER": { "REGEX": "(significant|major|important)"}}, {"OP": "?", "LOWER": {"REGEX": "(discover(y|ies)|findings?)"}}],
            [{"OP": "?", "LOWER": {"REGEX": "(obvious|extraordinary|exceptional|particular|undoubted|great|major)"}}, { "LOWER": {"REGEX": "(significance|importance)"}}],
            [{"LOWER": "earliest"}, {"LOWER": "dated"}],
            [{"OP": "?", "LOWER":  {"REGEX": "(important|excellent)"}}, {"LOWER": {"REGEX": "insights?"}}],
            [{"LOWER": "exceptionally"}, {"LOWER": "rich"}],
            [{"LOWER": "extraordinary"}, {"LOWER": "assemblage"}],
            [{"LOWER": "enormous"}, {"LOWER": "feature"}],
            [{"OP": "?", "LOWER": "particularly"}, {"LOWER": "interesting"}],
            [{"LOWER": "evidence"}, {"LOWER": "highlights"}],
            [{"LOWER": "assemblage"}, {"LOWER": "is"}, {"LOWER": "important"}],
            [{"LOWER": "important"}, {"OP": "?", "LOWER": {"REGEX": "(assemblage|find(ing)?|evidence|discovery)"}}],
            [{"LOWER": "results"}, {"LOWER": "of"}, {"LOWER": "this"}, {"LOWER": {"REGEX": "(investigation|excavation)"}}],
            [{"LOWER": "principle"}, {"LOWER": {"REGEX": "(aims|features?)"}}],
            [{"LOWER": "principal"}, {"LOWER": {"REGEX": "(aims|features?)"}}],
            [{"OP": "?", "LOWER": "more"}, {"LOWER": "substantial"}, {"OP": "?", "LOWER": "activity"}],
            [{"LOWER": {"REGEX": "(main|major)"}}, {"LOWER": "phase"}],
            [{"LOWER": "strongly"}, {"LOWER": {"REGEX": "(hints|suggests)"}}],
            [{"LOWER": "first"}, {"LOWER": "record"}, {"LOWER": "of"}],
            [{"LOWER": "not"}, {"LOWER": "typically"}, {"LOWER": "found"}],
            [{"LOWER": "unique"}, {"LOWER": "in"}, {"LOWER": "britain"}],
            [{"LOWER": "radio"}, {"OP": "?", "ORTH": "-"}, {"LOWER": "carbon"}, {"OP": "?", "LOWER": {"REGEX": "dat(ing|ed|e)"}}],
            [{"LOWER": "most"}, {"LOWER": {"REGEX": "important(ly)?"}}],
            [{"LOWER": {"REGEX": "strong(er)?"}}, {"LOWER": "evidence"}, {"OP": "?", "LOWER": {"REGEX": "(for|of)"}}],
            [{"LOWER": "carbon"}, {"LOWER": {"REGEX": "dat(s|e|ing|ed)"}}],
            [{"LOWER": "rare"}, {"LOWER": "example"}, {"OP": "?", "LOWER": "of"}],
            [{"LOWER": {"REGEX": "(strong(er|ly)?|considerable|important|plentiful)"}}, {"LOWER": "evidence"}],           
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
        sections: list = []
        #max_proximity: int = 3, 
        #significance_weight: float = 1.0, 
        #significance_terms: list = []
        ) -> None:

        self.nlp: Language = nlp
        self.spans_key: str = spans_key.strip()
        self.sections: list = sections
        #self.max_proximity: int = max_proximity
        #self.significance_weight: float = significance_weight
        #self.significance_terms: list = list(map(lambda s: s.strip().lower(), significance_terms))
        

    # multiple metrics to run, scores asdded to indicidual spans
    def __call__(self, doc: Doc) -> Doc:
        doc = self.set_section_scores(doc)
        doc = self.set_frequency_scores(doc)        
        doc = self.set_neg_proximity_scores(doc)
        doc = self.set_sig_proximity_scores(doc)
        doc = self.set_sig_sentence_scores(doc)
        return doc 


    @staticmethod
    def get_section_score_by_type(section_type: str="") -> float:
        sec_score = 0.0
        sec_type = section_type.strip().lower()

        if sec_type == "title":
            sec_score = 10.0
        elif sec_type == "abstract":
            sec_score = 1.0
        elif sec_type == "body":
            sec_score = 0.1
        elif sec_type == "end_material":
            sec_score = 0.0
        else:
           sec_score = 0.0

        return sec_score


    # scoring for the section the span occurs within
    def set_section_scores(self, doc: Doc) -> Doc:
         # ensure the custom properties exist before use
        if not Span.has_extension("sec_score"):
            Span.set_extension("sec_score", default=0.0)

        if not Span.has_extension("sections"):
            Span.set_extension("sections", default="")

        # get all the current spans
        all_spans = list(doc.spans.get(self.spans_key, []))
        if len(all_spans) < 1: return doc

        all_sections = self.sections
        if len(all_sections) < 1: return doc

        for span in all_spans:
            # find any sections containing the span
            containing_sections = [s for s in all_sections if s.get("start", span.end_char) <= span.start_char and s.get("end", span.start_char) >= span.end_char]
            if len(containing_sections) == 0:
                continue
            
            section_types: list[str] = list(set(map(lambda s: s.get("type", ""), containing_sections)))
            section_scores: list[float] = list(map(lambda t: self.get_section_score_by_type(t), section_types))           
            span._.sec_score = max(section_scores)
            span._.sections = ", ".join(section_types)
        return doc
       

    # scoring for frequency of occurrence of the concept
    def set_frequency_scores(self, doc: Doc) -> Doc:
        # ensure that custom properties exist before use
        if not Span.has_extension("occurrences"):
            Span.set_extension("occurrences", default=0)   

        if not Span.has_extension("frequency_by_label"):
            Span.set_extension("frequency_by_label", default=0.0)

        if not Span.has_extension("frequency_overall"):
            Span.set_extension("frequency_overall", default=0.0)

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
            span._.frequency_by_label = float(id_count) / float(lbl_count)
            span._.frequency_overall = float(id_count) / float(len(all_spans))
            span._.frequency_explain = f"id_count={id_count}, lbl_count={lbl_count}, all_count={len(all_spans)}"
        return doc
    

    # get textual context around a span
    @staticmethod
    def get_span_context(span: Span, window_size: int=4) -> str:
        doc = span.doc
        start = max(span.start - window_size, 0)
        end = min(span.end + window_size, len(doc))
        context_span = doc[start:end]
        return context_span.text


     # scoring for being in sentence containing 'significant' terms or phrases
    def set_sig_sentence_scores(self, doc: Doc) -> Doc:
        property_name = "sig_sentence"
        if not Span.has_extension(property_name):
            Span.set_extension(property_name, default=0.0)

        all_spans = list(doc.spans.get(self.spans_key, []))
        if len(all_spans) < 1: return doc

        # get sentences containing significant terms or phrases        
        matcher = SignificanceMatcher(doc.vocab)        
        matches = matcher(doc)
        sentences = set(map(lambda m: m.sent, matches))

        for span in all_spans:
            if span.sent in sentences:
                setattr(span._, property_name, 0.2)
        
        return doc


    # scoring for proximity to a 'significant' term or phrase
    def set_sig_proximity_scores(self, doc: Doc) -> Doc:
        matcher = SignificanceMatcher(doc.vocab)        
        matches = matcher(doc)      
        self.set_proximity_scores(doc, list(matches), max_proximity=4, property_name="sig_proximity", property_score=0.5)
        return doc
    

    # scoring for proximity to a 'negation' term or phrase
    def set_neg_proximity_scores(self, doc: Doc) -> Doc:
        matcher = NegationMatcher(doc.vocab)        
        matches = matcher(doc)
        self.set_proximity_scores(doc, list(matches), max_proximity=3, property_name="neg_proximity", property_score=1.0)
        return doc
        

    def set_proximity_scores(
        self, 
        doc: Doc, 
        proximity_to: list[Span], 
        max_proximity: int=4, 
        property_name: str="unknown", 
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
    

    # not used now - totals calculated in DocSummary
    #def set_overall_scores(self, doc: Doc):
        # ensure that custom properties exist before use
        #if not Span.has_extension("score"):
            #Span.set_extension("score", default=0.0) 

        #if not Span.has_extension("score_explain"):
            #Span.set_extension("score_explain", default="") 

        # get all the current spans
        #all_spans = list(doc.spans.get(self.spans_key, []))
        #if len(all_spans) == 0: return doc

        #con_weight = 1.0    # weighting for concept
        #sec_weight = 1.0    # weighting for section score
        #sig_weight = 1.0    # weighting for significance score
        #neg_weight = 0.0    # weighting for negation

        #for span in all_spans:
            #con_score = 1.0 # instance of concept
            #frequency = getattr(span._, "frequency_overall", 0.0)
            #sec_score = getattr(span._, "sec_score", 0.0)
            #sig_score = max(getattr(span._, "sig_proximity", 0.0), getattr(span._, "sig_sentence", 0.0))
            #neg_score = getattr(span._, "neg_proximity", 0.0)
            #tot_score = (con_weight * frequency * con_score) + (sec_weight * sec_score) + (sig_weight * sig_score)
            #tot_score_explain = f"(({con_weight} * {frequency} * {con_score}) + ({sec_weight} * {sec_score}) + ({sig_weight} * {sig_score}))"
            # note: neg_weight and neg_score not used in calculation yet

            #setattr(span._, "score", tot_score)
            #setattr(span._, "score_explain", tot_score_explain)

        #return doc
     

@Language.factory(name="span_scorer", default_config={"spans_key": DEFAULT_SPANS_KEY, "sections": []}) 
def create_span_scorer(
    nlp: Language, 
    name: str="span_scorer", 
    spans_key: str=DEFAULT_SPANS_KEY,
    sections: list=[]) -> Pipe:
    return SpanScorer(nlp, spans_key=spans_key, sections=sections)


# test the span_scorer pipeline component
if __name__ == "__main__":
    import spacy

    # TODO: get PDF files from URL, integrate mark's PDF to text script everywhere (cache the text),
    BASE_PATH = "./data/oasis/journals_july_2024/text_extraction-20251117/"

    # build the pipeline
    nlp = spacy.load("en_core_web_sm", disable=["ner"]) 
    nlp.add_pipe("normalize_text", before = "tagger")
    nlp.add_pipe("yearspan_ruler", last=True)
    nlp.add_pipe("periodo_ruler", last=True, config={"periodo_authority_id": "p0kh9ds"}) 
    nlp.add_pipe("fish_archobjects_ruler", last=True)
    nlp.add_pipe("child_span_remover", last=True) 
    nlp.add_pipe("span_scorer", last=True, config={"sections": []})
    # note could also call it after main pipeline runs, like this:
    # scorer = SpanScorer(nlp)
    # doc = scorer(doc)

    file_names = [
        "text_extraction_120_031_097.pdf.json",
        "text_extraction_2022_96_001_012_Cooper_Garton.pdf.json",
        "text_extraction_2022_96_013-068_Huxley.pdf.json",
        "text_extraction_archael547-005-040-breeze.pdf.json",
        "text_extraction_archael547-079-116-ceolwulf.pdf.json",
        "text_extraction_DAJ_v023_1901_040-047.pdf.json",
        "text_extraction_DAJ_v106_1986_018-100.pdf.json",
        "text_extraction_SAC118_Garton.pdf.json",
        "text_extraction_surreyac103_091-172_haslam.pdf.json",
        "text_extraction_surreyac103_185-266_saxby.pdf.json"        
    ]

    for file_name in file_names:
        file_path = os.path.join(BASE_PATH, file_name)        
        print(f"reading \"{file_path}\"")
        
        with open(file_path, "r") as f:
            if(file_name.lower().endswith(".json")):
                input_file_content = json.load(f)
            else:     
                input_text = f.read()           
                input_file_content = {"text": input_text}


        # run the pipeline on the text and get all identified spans
        print(f"processing text through pipeline")
        doc = nlp(input_file_content.get("text", ""))   

        
        # add any 'sections' from the input data file (for later scoring)
        #sections_as_spans = []
        #for section in input_file_content.get("sections", []):            
            #span = doc.char_span(section.get("start", 0), section.get("end", 0), label=section.get("type", "unknown"))
            #print(f"section: [{span.start_char}:{span.end_char}] \"{span.label_}\"")
            #if span is not None:
                #sections_as_spans.append(span)
        #doc.spans["sections"] = sections_as_spans

        #print(f"sections:\n{doc.spans["sections"]}")
        
        matcher = SignificanceMatcher(nlp.vocab)    
        sig_spans = matcher(doc)
        #print("Significance spans:")
        #for span in sig_spans:
            #print(f"[{span.start}:{span.end -1}] {span.text}")

        matcher = NegationMatcher(nlp.vocab)    
        neg_spans = matcher(doc)
        #print("Negation spans:")
        #for span in neg_spans:
            #print(f"[{span.start}:{span.end - 1}] {span.text}")

        # add scores
        sections = list(input_file_content.get("sections", []))
        scorer = SpanScorer(nlp, sections=sections)
        doc = scorer(doc)

        
        # output the results        
        summary = DocSummary(doc)
        output_file_name = os.path.join(BASE_PATH, f"span_scoring_output_{file_name}.csv")
        print("Writing output to ", output_file_name)
        with open(output_file_name, "w") as f:
            summary.spans_to_csv(file=f)
