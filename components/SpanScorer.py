"""
=============================================================================
Package :   rematch2
Module  :   SpanScorer.py
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Summary :   Score spans based on proximity to 'significant' terms.
Imports :   spacy, Doc, Span, Pipe, Matcher,Language, Vocab, Counter
Example :   nlp.add_pipe("span_scorer", last=True, config={"sections": []})
            # note could also call it after main pipeline runs, like this:
            # scorer = SpanScorer(nlp, sig_score=1.0, neg_score=1.0, sections=[]); 
            # doc = scorer(doc);         
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History :   
07/01/2024 CFB Initially created script
14/05/2026 CFB Updated to be more configurable, removed redundant code
=============================================================================
"""
import spacy, os, json
from collections import Counter
#from typing import Iterable, Any, cast

from spacy.tokens import Doc, Span
from spacy.pipeline import Pipe
from spacy.language import Language

from .Util import DEFAULT_SPANS_KEY
from .SpanRelationship import span_before, span_after, span_meets, span_met_by
from .spacypatterns import patterns_en_SIGNIFICANCE, patterns_en_NEGATION
from .DocSummary import DocSummary
from .BaseMatcher import BaseMatcher   

# default values for config parameters 
# (can be overridden using the component)
DEFAULT_MAX_PROXIMITY=3
DEFAULT_SIG_SCORE=1.0
DEFAULT_NEG_SCORE=1.0
DEFAULT_TITLE_SCORE=40.0
DEFAULT_ABSTRACT_SCORE=2.0
DEFAULT_BODY_SCORE=0.1
DEFAULT_END_MATTER_SCORE=0.0

class SpanScorer(Pipe):    
        
    def __init__(self, 
        nlp: Language, 
        spans_key: str = DEFAULT_SPANS_KEY, 
        max_proximity: int = DEFAULT_MAX_PROXIMITY,
        sig_score: float = DEFAULT_SIG_SCORE,
        neg_score: float = DEFAULT_NEG_SCORE,
        title_score: float = DEFAULT_TITLE_SCORE,
        abstract_score: float = DEFAULT_ABSTRACT_SCORE,
        body_score: float = DEFAULT_BODY_SCORE,
        end_matter_score: float = DEFAULT_END_MATTER_SCORE,
        sections: list = [],        
        ) -> None:

        self.nlp: Language = nlp
        self.spans_key: str = spans_key.strip()
        self.sections: list = sections
        self.max_proximity: int = max_proximity
        self.sig_score: float = sig_score
        self.neg_score: float = neg_score
        self.title_score: float = title_score
        self.abstract_score: float = abstract_score
        self.body_score: float = body_score
        self.end_matter_score: float = end_matter_score

    # run multiple metrics, add scores to individual spans
    def __call__(self, doc: Doc) -> Doc:
        doc = self.set_section_scores(doc)
        doc = self.set_frequency_scores(doc)        
        doc = self.set_neg_proximity_scores(doc)
        doc = self.set_sig_proximity_scores(doc)
        #doc = self.set_sig_sentence_scores(doc)
        doc = self.set_overall_span_scores(doc)
        return doc 


    def get_section_score_by_type(self, sec_type: str="") -> float:
        sec_score = 0.0
        
        match sec_type.strip().lower():
            case "title":
                sec_score = self.title_score
            case "abstract":
                sec_score = self.abstract_score
            case "body":
                sec_score = self.body_score
            case "end_matter":
                sec_score = self.end_matter_score
            case _:
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
            # list the sections this span is part of (e.g ['page', 'body'])
            section_types: list[str] = list(set(map(lambda s: s.get("type", ""), containing_sections)))
            # override - if section_types does not include any known type except page, then assume 'body'
            if all(st not in ["title", "abstract", "body", "end_matter"] for st in section_types):
                section_types.append("body")                     
                        
            # get the highest section score for these sections
            section_scores: list[float] = list(map(lambda t: self.get_section_score_by_type(t), section_types))           
            # assign the highest section score and list of sections to the span
            span._.sec_score = max(section_scores)
            span._.sections = ", ".join(section_types)
        return doc
       

    # scoring for frequency of occurrence of the concept
    def set_frequency_scores(self, doc: Doc) -> Doc:
        # ensure all required custom properties exist before use
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

        # if none, nothing to score so return the doc
        if len(all_spans) < 1: return doc

        # count occurrences by id (or text if no id) and by label
        ident_count = Counter(map(lambda s: s.text.lower() if not s.id else s.id, all_spans))
        label_count = Counter(map(lambda s: s.label, all_spans))
        
        # set scores on each span
        for span in all_spans:
            id: str = span.text.lower() if not span.id else span.id
            lbl: str = span.label
            id_count: int = ident_count.get(id, 0) 
            lbl_count: int = label_count.get(lbl, 1) # 1 avoids divide by zero error
            span._.occurrences = id_count
            span._.frequency_by_label = float(id_count) / float(lbl_count)
            span._.frequency_overall = float(id_count) / float(len(all_spans))
            span._.frequency_explain = f"id_count={id_count}, lbl_count={lbl_count}, all_count={len(all_spans)}"
        return doc
    

    # get textual context around a span - for display/reporting purposes
    @staticmethod
    def get_span_context(span: Span, window_size: int=4) -> str:
        doc = span.doc
        start = max(span.start - window_size, 0)
        end = min(span.end + window_size, len(doc))
        context_span = doc[start:end]
        return context_span.text

    # set span context for all spansm for display/reporting purposes 
    def set_span_contexts(self, doc: Doc, window_size: int=4) -> Doc:
        # ensure the custom property exists before use
        if not Span.has_extension("context"):
            Span.set_extension("context", default="")

        # get all the current spans
        all_spans = list(doc.spans.get(self.spans_key, []))
        if len(all_spans) < 1: return doc

        for span in all_spans:
            span._.context = self.get_span_context(span, window_size=window_size)

        return doc

     # scoring for being in sentence containing 'significant' terms or phrases
     # (not used now, using proximity instead)
    """ def set_sig_sentence_scores(self, doc: Doc) -> Doc:
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
        
        return doc """


    # scoring for proximity to a 'significant' term or phrase
    def set_sig_proximity_scores(self, doc: Doc) -> Doc:
        matcher = BaseMatcher(doc.vocab)   
        matcher.add_patterns("significance", patterns_en_SIGNIFICANCE) 
        matches = matcher(doc)      
        self.set_proximity_scores(doc, 
            proximity_to=list(matches), 
            max_proximity=self.max_proximity, 
            property_name="sig_proximity", 
            property_score=self.sig_score
        )
        return doc
    

    # scoring for proximity to a 'negation' term or phrase
    def set_neg_proximity_scores(self, doc: Doc) -> Doc:
        matcher = BaseMatcher(doc.vocab)   
        matcher.add_patterns("negation", patterns_en_NEGATION)         
        matches = matcher(doc)
        self.set_proximity_scores(doc, 
            proximity_to=list(matches), 
            max_proximity=self.max_proximity, 
            property_name="neg_proximity", 
            property_score=self.neg_score
        )
        return doc
        

    def set_proximity_scores(self, 
        doc: Doc, 
        proximity_to: list[Span], 
        max_proximity: int=1, 
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
    
    
    def set_overall_span_scores(self, doc: Doc):
        # ensure that custom properties exist before use
        if not Span.has_extension("score"):
            Span.set_extension("score", default=0.0) 

        if not Span.has_extension("score_explain"):
            Span.set_extension("score_explain", default="") 

        # get all the current spans
        all_spans = list(doc.spans.get(self.spans_key, []))
        if len(all_spans) == 0: return doc
        
        for span in all_spans:
            sec_score = getattr(span._, "sec_score", 0.0)
            sig_score = getattr(span._, "sig_proximity", 0.0)
            score = sec_score + sig_score 
            score_explain = f"({sec_score:.2f}) + ({sig_score:.2f})"
            setattr(span._, "score", score)
            setattr(span._, "score_explain", score_explain)

        return doc
     

@Language.factory(
    name="span_scorer", 
    default_config={
        "spans_key": DEFAULT_SPANS_KEY, 
        "max_proximity": DEFAULT_MAX_PROXIMITY,
        "sig_score": DEFAULT_SIG_SCORE,
        "neg_score": DEFAULT_NEG_SCORE,
        "sections": []
}) 
def create_span_scorer(
    nlp: Language, 
    name: str="span_scorer", 
    spans_key: str=DEFAULT_SPANS_KEY,
    max_proximity: int=DEFAULT_MAX_PROXIMITY,
    sig_score: float=DEFAULT_SIG_SCORE,
    neg_score: float=DEFAULT_NEG_SCORE,
    sections: list=[]
    ) -> Pipe:
    return SpanScorer(nlp, 
        max_proximity=max_proximity,
        sig_score=sig_score,
        neg_score=neg_score,
        spans_key=spans_key, 
        sections=sections)


# test the span_scorer pipeline component
if __name__ == "__main__":
    import spacy

    # TODO: get PDF files from URL, integrate mark's PDF to text script everywhere (cache the text),
    BASE_PATH = "./data/oasis/journals_july_2024/text_extraction-20251117/"

    # build the configured pipeline
    nlp = spacy.load("en_core_web_sm", disable=["ner"]) 
    nlp.add_pipe("text_normalizer", before = "tagger")
    nlp.add_pipe("yearspan_ruler", last=True)
    nlp.add_pipe("periodo_ruler", last=True, config={"periodo_authority_id": "p0kh9ds"}) 
    nlp.add_pipe("vocabulary_ruler", 
        name = "object_types_ruler", last = True, 
        config = {
            "default_label": "FISH_OBJECT",
            "token_pos": ["NOUN"],
            "patt_list": json.load(open("./vocabularies/patterns_FISH_mda_obj_20260513.json"))            
        }
    ) 
    nlp.add_pipe("child_span_remover", last=True) 
    # nlp.add_pipe("span_scorer", last=True, config={"sig_score": 1.0, "neg_score": 1.0, "sections": []})
    # note could also call it after main pipeline runs, like this:
    # scorer = SpanScorer(nlp, sig_score=1.0, neg_score=1.0, sections=[]); doc = scorer(doc);

    file_names = [
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
