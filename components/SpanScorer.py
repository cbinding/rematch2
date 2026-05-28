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
import spacy, os, mimetypes, json
from collections import Counter
#from typing import Iterable, Any, cast

from spacy.tokens import Doc, Span
from spacy.pipeline import Pipe
from spacy.language import Language

from .SpanRelationship import span_before, span_after, span_meets, span_met_by
from .spacypatterns import patterns_en_SIGNIFICANCE, patterns_en_NEGATION
from .DocSummary import DocSummary
from .BaseMatcher import BaseMatcher   

# default values for config parameters (can be overridden using the component)
from .Util import DEFAULT_SPANS_KEY
DEFAULT_SIG_PROXIMITY: int=3 # proximity in number of tokens between span and 'significant' term to count as 'nearby' for scoring purposes
DEFAULT_NEG_PROXIMITY: int=3 # proximity in number of tokens between span and 'negation' term to count as 'nearby' for scoring purposes
DEFAULT_SIG_SCORE: float=1.0 # score to assign to span if it is within specified token proximity of a 'significant' term or phrase 
DEFAULT_NEG_SCORE: float=1.0 # score to assign to span if it is within specified token proximity of a 'negation' term or phrase
DEFAULT_SEC_SCORES: dict[str, float|int]={
    "title": 40.0, # high score for title as likely to contain key info about the content of the article
    "abstract": 2.0, # moderate score for abstract as likely to contain key info about the content of the article
    "body": 0.1, # low score for body as likely to contain a lot of less important info, but still some key info may be found here
    "end_matter": 0.0 # no score for end matter as unlikely to contain key info about the content of the article
}

class SpanScorer(Pipe):    
        
    def __init__(self, 
        nlp: Language, 
        spans_key: str = DEFAULT_SPANS_KEY, 
        sig_proximity: int = DEFAULT_SIG_PROXIMITY,
        neg_proximity: int = DEFAULT_NEG_PROXIMITY,
        sig_score: float = DEFAULT_SIG_SCORE,
        neg_score: float = DEFAULT_NEG_SCORE,
        sec_scores: dict[str, float|int] = DEFAULT_SEC_SCORES.copy(),
        sections: list = [],        
        ) -> None:

        self.nlp: Language = nlp
        self.spans_key: str = spans_key.strip()
        self.sections: list = sections
        self.sig_proximity: int = sig_proximity
        self.neg_proximity: int = neg_proximity
        self.sig_score: float = sig_score
        self.neg_score: float = neg_score
        # merge new scores with defaults, allowing overrides of default scores
        self.sec_scores: dict[str, float|int] = DEFAULT_SEC_SCORES.copy()
        self.sec_scores.update(sec_scores) 

    # run multiple metrics, add scores to individual spans
    def __call__(self, doc: Doc) -> Doc:
        doc = self.set_section_scores(doc)
        doc = self.set_frequency_scores(doc)        
        doc = self.set_neg_proximity_scores(doc)
        doc = self.set_sig_proximity_scores(doc)
        #doc = self.set_sig_sentence_scores(doc)
        doc = self.set_overall_span_scores(doc)
        return doc 
    

    # scoring for the section the span occurs within
    def set_section_scores(self, doc: Doc) -> Doc:
         # ensure the custom properties exist before use
        if not Span.has_extension("sec_score"):
            Span.set_extension("sec_score", default=0.0)

        if not Span.has_extension("sections"):
            Span.set_extension("sections", default="")

        # get the current spans. If none, nothing to score so return the doc. 
        all_spans = list(doc.spans.get(self.spans_key, []))
        if len(all_spans) < 1: return doc

        all_sections = self.sections
        if len(all_sections) < 1: return doc

        for span in all_spans:
            # identify any sections containing this span            
            def span_is_within(section):
                return section.get("start", span.end_char) <= span.start_char \
                   and section.get("end", span.start_char) >= span.end_char    
                        
            containing_sections = [sec for sec in all_sections if span_is_within(sec)]

            # if no sections contain this span, leave score as default and continue            
            if len(containing_sections) == 0:
                continue

            # list the sections this span is part of (e.g ['page', 'abstract', 'body'])
            containing_section_types: list[str] = list(set(map(lambda s: s.get("type", ""), containing_sections)))

            # if section_types does not include ANY known type except 'page', then assume 'body'
            if all(section_type not in list(self.sec_scores) for section_type in containing_section_types):
                containing_section_types.append("body")                     
                        
            # assign to the span the highest section score for the containing sections
            get_sec_score = lambda t: self.sec_scores.get(t.strip().lower(), 0.0)
            span._.sec_score = max(map(get_sec_score, containing_section_types))
            span._.sections = ", ".join(containing_section_types)            
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
        
        # set frequency scores on each span
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
    

    # get textual context around a span for display/reporting purposes
    # window_size is no of tokens to include before and after the span 
    @staticmethod
    def get_span_context(span: Span, window_size: int=4) -> str:
        doc = span.doc
        start = max(span.start - window_size, 0)
        end = min(span.end + window_size, len(doc))
        context_span = doc[start:end]
        return context_span.text

    # set 'context' for all spans (the textual context immediately surrounding the span) 
    # for display/reporting purposes to show the span in textual context (e.g. in a report or UI) 
    # note this is not used for scoring, just to provide additional info about the span in outputs 
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
            max_proximity=self.sig_proximity, 
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
            max_proximity=self.neg_proximity, 
            property_name="neg_proximity", 
            property_score=self.neg_score
        )
        return doc
        

    def set_proximity_scores(self, 
        doc: Doc, 
        proximity_to: list[Span], 
        max_proximity: int=1, 
        property_name: str="proximity_score", 
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
                #span._[clean_property_name] = property_value # this syntax doesnt work

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
            #neg_score = getattr(span._, "neg_proximity", 0.0)
            score = sec_score + sig_score #- neg_score
            # not currently using the neg_acore va;lue in overall scoring
            #score_explain = f"({sec_score:.2f}) + ({sig_score:.2f}) - ({neg_score:.2f})"
            score_explain = f"({sec_score:.2f}) + ({sig_score:.2f})"
            setattr(span._, "score", score)
            setattr(span._, "score_explain", score_explain)

        return doc
     

@Language.factory(
    name="span_scorer", 
    default_config={
        "spans_key": DEFAULT_SPANS_KEY, 
        "sig_proximity": DEFAULT_SIG_PROXIMITY,
        "neg_proximity": DEFAULT_NEG_PROXIMITY,
        "sig_score": DEFAULT_SIG_SCORE,
        "neg_score": DEFAULT_NEG_SCORE,
        "sec_scores": DEFAULT_SEC_SCORES.copy(),
        "sections": []
}) 
def create_span_scorer(
    nlp: Language, 
    name: str="span_scorer", 
    spans_key: str=DEFAULT_SPANS_KEY,
    sig_proximity: int=DEFAULT_SIG_PROXIMITY,
    neg_proximity: int=DEFAULT_NEG_PROXIMITY,
    sig_score: float=DEFAULT_SIG_SCORE,
    neg_score: float=DEFAULT_NEG_SCORE,
    sec_scores: dict[str, float|int] = DEFAULT_SEC_SCORES.copy(),
    sections: list=[]
    ) -> Pipe:
    return SpanScorer(nlp, 
        sig_proximity=sig_proximity,
        neg_proximity=neg_proximity,
        sig_score=sig_score,
        neg_score=neg_score,
        spans_key=spans_key, 
        sec_scores=sec_scores, 
        sections=sections)


# to test this module independently, run from package root:
# python -m components.SpanScorer
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

    #nlp.add_pipe("span_scorer", last=True, config={"sig_score": 1.0, "sec_scores": {}, "sections": []})
    # note could also call it after main pipeline runs, like this:
    # scorer = SpanScorer(nlp, sig_score=1.0, sections=[]); doc = scorer(doc);

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
        input_file_path = os.path.join(BASE_PATH, file_name)        
        print(f"reading \"{input_file_path}\"")
        
        with open(input_file_path, "r") as f:
            input_file_type = mimetypes.guess_type(input_file_path)
            input_file_ext =  os.path.splitext(file_name.strip().lower())  
            input_file_content = {}

            if input_file_type == "application/pdf" or input_file_ext == "pdf":     
                print(f"PDF file detected, but PDF parsing not implemented in this test script. Skipping file: {file_name}")
                continue
            elif input_file_type == "application/json" or input_file_ext == "json":            
                input_file_content = json.load(f)
            elif input_file_type == "text/plain" or input_file_ext == "txt":     
                input_file_content = {"text": f.read()}
            else:
                print(f"Unsupported file type: {file_name}")
                continue

        # run the pipeline on the text and get all identified spans
        print(f"processing text through pipeline")
        doc = nlp(input_file_content.get("text", ""))   
                       
        # add scores, use sections (if present) to enhance score
        sections = list(input_file_content.get("sections", []))
        scorer = SpanScorer(nlp, sections=sections)
        doc = scorer(doc)
        
        # output the results        
        summary = DocSummary(doc)
        output_file_name = os.path.join(BASE_PATH, f"span_scoring_output_{file_name}.csv")
        print("Writing output to ", output_file_name)
        with open(output_file_name, "w") as f:
            summary.spans_to_csv(file=f)
