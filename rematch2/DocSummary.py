"""
=============================================================================
Package   : rematch2
Module    : DocSummary.py
Classes   : DocSummary
Project   : Any
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : Convert spaCy Doc spans, tokens, pairs, counts to
            various output formats. use to improve consistency            
Imports   : escape, pandas, DataFrame, Doc, displacy, SpanPairs
Example   : html = DocSummary(doc).spans_to_html()
    .doctext, .tokens, .spans, .span_scores, .labels, .label_counts, .spanpairs 
License   : https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History
14/03/2024 CFB consolidated and centralized code from other scripts
=============================================================================
"""
from html import escape
from functools import cached_property
import json
import os
from pathlib import Path
import pandas as pd
import spacy
from html import escape  # for writing escaped HTML
from pandas import DataFrame
from spacy.tokens import Doc, Span, Token
from spacy import displacy
from .SpanPair import SpanPair
from .SpanPairs import SpanPairs
from .Decorators import run_timed
from .Util import DEFAULT_SPANS_KEY
from collections import Counter

class DocSummary:

    def __init__(
            self, 
            doc: Doc, # required
            spans_key: str=DEFAULT_SPANS_KEY, 
            metadata: dict[str, str] = {}            
        ):
        self._doc = doc
        self._spans_key = spans_key.strip()
        self._metadata = metadata

        # copy any entities to spans so they can be reported and displayed
        # in the same way as all other spans identified
        #for ent in doc.ents: doc.spans[spans_key].append(ent)            

        # calculate and attach concept frequency (similar to term frequency)
        #self._calculate_concept_frequency() 


    @staticmethod
    def _id_for_span(span: Span) -> str:
        id: str = "other"
        span_id: str = span.id_.strip()
        span_text: str = span.text.strip()

        if len(span_id) > 0:
            id = span_id
        elif len(span_text) > 0:
            id = span_text
        
        return id
 

    @property
    def metadata(self) -> dict[str,str]: 
        return self._metadata
    

    @property
    def doctext(self) -> str:
      return self._doc.text
    

    @property
    def spans(self) -> list[Span]:
      spans = self._doc.spans.get(self._spans_key, [])
      return spacy.util.filter_spans(spans)


    @property
    def tokens(self) -> list[Token]:
        return [t for t in self._doc]
    

    @cached_property
    def span_pairs(self) -> list[SpanPair]:
        pairs = self.get_span_pairs()
        return pairs

    @cached_property
    def span_scores(self) -> list:
        scores = self.get_span_scores() 
        return scores


    @cached_property
    def label_counts(self) -> dict[str, dict]:
        counts = self.get_span_counts_by_label()
        return counts

    @cached_property
    def negated_pairs(self) -> list[SpanPair]:
        pairs = self.get_negated_span_pairs()
        return pairs

    def __str__(self):
        return self.doctext


    def __repr__(self):
        return self.__str__()

             
    def metadata_to_html(self) -> str:
        html = []
        html.append("<ul>")
        for key, val in self._metadata.items():
            html.append(f"<li>")
            html.append(f"<strong>{escape(key)}:</strong>")
            if isinstance(val, str):
                html.append(escape(val))               
            else:
                html.append(str(val))
            html.append('</li>')            
        html.append("</ul>")

        # finally join and return
        return f"\n".join(html)


    def metadata_to_json(self) -> str:
        return json.dumps(data)


    def metadata_to_text(self) -> str:
        text = []
        for key, val in self._metadata.items():
            text.append(f"* {key}: {str(val)}")
            
        return f"\n".join(text)

    
    def doctext_to_text(self) -> str: return self._doc.text

    def doctext_to_html(
        self,
        options: dict={}, 
        exclude: list=[
            "DATEPREFIX", 
            "DATESUFFIX", 
            "DATESEPARATOR", 
            "ORDINAL", 
            "MONTHNAME", 
            "SEASONNAME"
        ]) -> str:

        default_options = { 
            "colors": { 
                "GPE": "palegreen",
                "PLACE": "palegreen",
                "NEGATION": "lightgray",
                "PERIOD": "yellow", 
                "YEARSPAN": "moccasin", 
                "AAT_OBJECT": "plum",
                "AAT_ACTIVITY": "lightsalmon",
                "FISH_OBJECT": "plum",
                "FISH_MONUMENT": "lightblue",
                "FISH_ARCHSCIENCE": "lightpink",
                "FISH_ACTIVITY": "lightsalmon",
                "FISH_EVIDENCE": "aliceblue",
                "FISH_MATERIAL": "palegreen",
                "FISH_EVENTTYPE": "coral"
            } 
        }
    
        # create temp subset (as options don't specify what to show/exclude)
        self._doc.spans["temp_subset"] = list(filter(lambda span: span.label_ not in exclude, self.spans))

        # create HTML string rendering the document text with highlighted spans       
        html = displacy.render(
            docs = self._doc,
            style = "span", 
            page = False, 
            minify = False, 
            jupyter = False, 
            options = default_options | options | {"spans_key": "temp_subset"} # shallow merging
        )

        # remove the temp subset and return the HTML rendered string
        del self._doc.spans["temp_subset"]
        return html


    @run_timed
    def report(self, format: str="text") -> str: 
        match format.strip().lower():  
            case "html": return self.report_to_html()
            case "json": return self.report_to_json()
            case "text": return self.report_to_text()
            case _: return self.report_to_text()        
    
    
    @staticmethod
    def get_span_context(span: Span, window_size: int=4) -> str:
        doc = span.doc
        start = max(span.start - window_size, 0)
        end = min(span.end + window_size, len(doc))
        context_span = doc[start:end]
        return context_span.text
           

    def spans_to_df(self) -> DataFrame:

        return DataFrame([{
            "start": span.start_char,
            "end": span.end_char -1,
            "token_start": span.start,
            "token_end": span.end - 1,            
            "label": span.label_,
            "id": span.id_,
            "text": span.text,
            # if SpanScorer is in the pipeline, these custom attributes will be populated
            #"occurrences": getattr(span._, "ccurrences", 0), # number of occurrences
            #"frequency_by_label": getattr(span._, "frequency_by_label", 0.0), # concept frequency
            #"frequency_overall": getattr(span._, "frequency_overall", 0.0), # concept frequency
            #"frequency_explain": getattr(span._, "frequency_explain", ""),
            "sec_score": getattr(span._, "sec_score", 0.0), # section score
            "sections": getattr(span._, "sections", ""),
            "sig_sentence": getattr(span._, "sig_sentence", 0.0), # significance by sentence score
            "sig_proximity": getattr(span._, "sig_proximity", 0.0), # significance by proximity score
            #"llm_sig_score": span._.llm_sig_score if Span.has_extension("llm_sig_score") else 0.0, # llm significance score
            "neg_proximity": getattr(span._, "neg_proximity", 0.0), # negation by proximity score
            #"score": getattr(span._, "score", 0.0), # calculated score
            #"score_explain": getattr(span._, "score_explain", ""), # calculated score explanation for testing/debugging
            "context": DocSummary.get_span_context(span)
            } for span in self.spans]).drop_duplicates()


    def spans_to_csv(self, file=None, sep=",") -> str:
        df = self.spans_to_df()
        return df.to_csv(path_or_buf=file, sep=sep, index=False, header=True)


    def spans_to_html(self) -> str:
        df = self.spans_to_df()
        if df.empty:
            return "" 
        df["span"] = df.apply(lambda row: DocSummary._make_link(row["id"], row["text"]), axis=1)
        
        html = df.to_html(
            border=0,
            index=False, 
            justify="left",
            render_links=True, 
            escape=False,
            na_rep='',
            classes=['table', 'table-sm', 'table-striped', 'table-light']
        ) 
        return html 


    def spans_to_json(self) -> str:
        df = self.spans_to_df()
        return df.to_json(orient="records")


    def spans_to_list(self) -> list:
        df = self.spans_to_df()
        return df.to_dict(orient="records")


    def spans_to_text(self) -> str:
        df = self.spans_to_df()
        pd.set_option('display.max_colwidth', None)
        return(df.to_string(index=False)) if len(df) > 0 else "NO RECORDS" 


    @run_timed
    def get_span_pairs(
        self,
        left_labels: list=["PERIOD", "YEARSPAN", "FISH_MATERIAL"], 
        right_labels: list=["FISH_OBJECT", "FISH_MONUMENT"], 
        rel_ops: list=[ "<", ">", ".", ";" ]
        ) -> list[SpanPair]:

        pairs = SpanPairs(doc=self._doc, rel_ops=rel_ops, left_labels=left_labels, right_labels=right_labels).pairs

        return pairs


    @run_timed
    def get_negated_span_pairs(
        self,
        right_labels=["YEARSPAN", "PERIOD", "FISH_OBJECT", "FISH_MONUMENT", "FISH_MATERIAL"],
        rel_ops=["<", "."]        
        ) -> list[SpanPair]:

        pairs = SpanPairs(doc=self._doc, rel_ops=rel_ops, left_labels=["NEGATION"], right_labels=right_labels).pairs

        return pairs

    # return list [{id, label, text, score}, id, label, text, score}, ...] 
    # returned in descending count order - note there is probably a more elegant way to do this 
    def get_span_scores(
        self,            
        exclude: list = [
            "NEGATION", 
            "DATEPREFIX", 
            "DATESEPARATOR", 
            "DATESUFFIX", 
            "ORDINAL", 
            "MONTHNAME", 
            "SEASONNAME"
        ]) -> list:
        
        # create list of id, text[], label, count, score
        scores = {}

        con_weight: float = 1.0    # weighting for concept
        sec_weight: float = 1.0    # weighting for section score
        sig_weight: float = 1.0    # weighting for significance score
        neg_weight: float = 0.0    # weighting for negation

        # get all the current spans
        all_spans: list[Span] = list(self._doc.spans.get(self._spans_key, []))
        if len(all_spans) == 0: return list(scores.values())

        # count occurrences by id (or text if no id) and by label
        ident_count = Counter(map(lambda span: span.text.lower() if not span.id_ else span.id_, all_spans))
        label_count = Counter(map(lambda span: span.label_, all_spans))

        # build dict to hold scores for each span id
        for span in all_spans:
            # create new span record or increment existing
            id = span.text.lower() if not span.id_ else span.id_
            sec_score: float = getattr(span._, "sec_score", 0.0) # section score
            sig_sentence: float = getattr(span._, "sig_sentence", 0.0) # significance score
            sig_proximity: float = getattr(span._, "sig_proximity", 0.0) # significance score
            neg_proximity: float = getattr(span._, "neg_proximity", 0.0) # negation score
            significance: float = max(sig_sentence, sig_proximity)
            if id not in scores:
                scores[id] = { 
                    "id": id, 
                    "text": [span.text], 
                    "label": span.label_, 
                    "count": 1, 
                    "sec_score": sec_score, 
                    "sig_score": significance,
                    "neg_score": neg_proximity,
                    "score": 0, 
                    "score_explain": ""
                }
            else:
                if span.text not in scores[id]["text"]:
                    scores[id]["text"].append(span.text)
                scores[id]["count"] += 1
                scores[id]["sec_score"] += sec_score
                scores[id]["sig_score"] += significance
                scores[id]["neg_score"] += neg_proximity # neg score not currently used in calculation
                
        sum_sec_scores = sum(item["sec_score"] for item in scores.values())
        sum_sig_scores = sum(item["sig_score"] for item in scores.values())

        # now calculate and add scores
        for item in scores.values():
            id = item.get("id","")
            label = item.get("label","")
            id_count = ident_count.get(id, 0) 
            lbl_count = label_count.get(label, 0)            
            frequency_by_label: float = float(id_count) / float(lbl_count if lbl_count > 0 else 1)   
            frequency_overall: float = float(id_count) / float(len(all_spans))
            #item["score"] = (con_weight * item["count"] * frequency_by_label) + (sec_weight * item["sec_score"] * frequency_by_label) + (sig_weight * item["sig_score"] * frequency_by_label)
            #item["score_explain"] = f"(({con_weight} * {frequency_by_label}) + ({sec_weight} * {item["sec_score"]} * {frequency_by_label}) + ({sig_weight} * {item["sig_score"]} * {frequency_by_label}))"
            
            #item["score"] = (sec_weight * (item["sec_score"] / sum_sec_scores)) + (sig_weight * (item["sig_score"] / sum_sig_scores))
            #item["score_explain"] = f"(({sec_weight} * {"{:.3f}".format(item["sec_score"])} / {"{:.3f}".format(sum_sec_scores)}) + ({sig_weight} * {"{:.3f}".format(item["sig_score"])} / {"{:.3f}".format(sum_sig_scores)}))"
            
            item["score"] = (sec_weight * item["sec_score"]) + (sig_weight * item["sig_score"])
            item["score_explain"] = f"(({sec_weight} * {"{:.3f}".format(item["sec_score"])}) + ({sig_weight} * {"{:.3f}".format(item["sig_score"])}))"
            

        return list(scores.values()) # create list of id, text[], label, count, score


    def span_scores_to_df(self) -> DataFrame: 
        
        # sort the span score records
        sorted_list = sorted(self.span_scores, key=lambda x: (x.get("score", 0)), reverse=True)

        # return as dataframe
        return DataFrame([{
            "id": sc.get("id", ""),
            "label": sc.get("label", ""), 
            "text": r" / ".join(sc.get("text", [])),
            "count": int(sc.get("count", 0)),
            "score": sc.get("score", ""),
            "score_explain": sc.get("score_explain", ""),
            } for sc in sorted_list])


    def span_scores_to_csv(self, sep: str=",") -> str:
        df = self.span_scores_to_df()
        return df.to_csv(sep=sep)

    
    # use for combining columns to form an HTML anchor
    @staticmethod
    def _make_link(id, text):
            if id.startswith("http"):
                return f"<a target='_blank' rel='noopener noreferrer' href='{id}'>{escape(text)}</a>"
            else:
                return escape(text)
            

    def span_scores_to_html(self) -> str:
        df = self.span_scores_to_df()        
                    
        if df.empty:
            return "" 
        df["span"] = df.apply(lambda row: DocSummary._make_link(row["id"], row["text"]), axis=1)
        
        html = df.to_html(
            columns=["span", "label", "count", "score", "score_explain"],
            border=0,
            justify="left",
            index=False, 
            render_links=True, 
            escape=False,
            float_format=lambda x: "{:5.3f}".format(x),
            na_rep='',
            classes=['table', 'table-sm', 'table-striped', 'table-light']
        ) 
        return html  


    def span_scores_to_json(self) -> str:
        df = self.span_scores_to_df()
        return df.to_json(orient="records")


    def span_scores_to_text(self) -> str:
        df = self.span_scores_to_df()
        pd.set_option('display.max_colwidth', None)
        return(df.to_string(index=False)) if len(df) > 0 else "NO RECORDS" 

        
    # count spans by label, return list [{label, count}, {label, count}, ...] 
    # returned in descending count order
    def get_span_counts_by_label(
        self,
        exclude: list = [
            "NEGATION", 
            "DATEPREFIX", 
            "DATESEPARATOR", 
            "DATESUFFIX", 
            "ORDINAL", 
            "MONTHNAME", 
            "SEASONNAME"
        ]) -> dict[str, dict]:
         
        counts = {}

        for span in self.spans:
            label = span.label_
            # exclude specified labels from summary counts
            if label in exclude:
                continue            
            
            # create a new record if not encountered before, or increment the count
            if label not in counts:
                counts[label] =  { "label": label, "count": 1 }  
            else:
                counts[label]["count"] += 1            
        
        # return as list sorted by ascending count
        return counts


    def label_counts_to_df(self) -> DataFrame: 

        counts = sorted(list(self.label_counts.values()), key=lambda x: x.get("count", 0), reverse=True)

        # convert to DataFrame, casting count to int
        # (in case it is a float, e.g. if cf_value was used)
        return DataFrame([{
            "label": item.get("label", ""),
            "count": int(item.get("count", 0))
            } for item in counts]) 


    def label_counts_to_csv(self, sep: str=",") -> str:
        df = self.label_counts_to_df()
        return df.to_csv(sep=sep)


    def label_counts_to_html(self) -> str:
        df = self.label_counts_to_df()
        if df.empty: return "" 
                
        html = df.to_html(
            columns=["label", "count"],
            border=0,
            index=False, 
            render_links=True, 
            escape=False,
            na_rep='',
            classes=['table', 'table-sm', 'table-striped', 'table-light']
        ) 
        return html 

    
    def label_counts_to_json(self) -> str:
        df = self.label_counts_to_df()
        return df.to_json(orient="records")


    def label_counts_to_text(self) -> str:
        df = self.label_counts_to_df()
        pd.set_option('display.max_colwidth', None)
        return(df.to_string(index=False)) if len(df) > 0 else "NO RECORDS" 


    def tokens_to_df(self) -> DataFrame: 
        if len(self.tokens) == 0:
            return DataFrame(columns=["index", "start", "end", "pos", "text", "lemma"])
        else:
            return DataFrame([{
                "index": tok.i,
                "start": tok.idx + 1,
                "end": tok.idx + len(tok.text),
                "pos": tok.pos_,
                "text": tok.text,
                "lemma": tok.lemma_,
                } for tok in self.tokens])  
    

    def tokens_to_csv(self, sep: str=",") -> str:
        df = self.tokens_to_df()
        return df.to_csv(sep=sep)
            

    def tokens_to_html(self) -> str:
        df = self.tokens_to_df()
        html = df.to_html(
            border=0,
            index=False, 
            render_links=True, 
            escape=True,
            na_rep='',
            classes=['table', 'table-sm', 'table-striped', 'table-light']
        ) 
        return html 


    def tokens_to_list(self) -> list:
        df = self.tokens_to_df()
        return df.to_dict(orient="records")


    def tokens_to_json(self) -> str:
        df = self.tokens_to_df()
        return df.to_json(orient="records")


    def tokens_to_text(self) -> str:
        df = self.tokens_to_df()
        pd.set_option('display.max_colwidth', None)
        return(df.to_string(index=False)) if len(df) > 0 else "NO RECORDS"

   
    @run_timed
    def report_to_html(
        self,
        include_metadata: bool = True,
        include_doctext: bool = True,        
        include_tokens: bool = False,
        include_label_counts: bool = True, 
        include_spans: bool = False,        
        include_span_scores: bool = True,
        include_span_pairs: bool = True,
        include_negated_pairs: bool = False
        ) -> str:
        output = []

        # write header tags
        output.append("<!DOCTYPE html>")
        output.append("<html>")
        output.append("<head>")
        file_path = os.path.join(Path(__file__).parent, "DocSummary.css")
        with open(file_path, 'r', encoding='utf8') as css_file:
            css_text = css_file.read()
            output.append(f'<style>{css_text}</style>')    
        output.append(" <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/css/bootstrap.min.css' rel='stylesheet' integrity='sha384-LN+7fdVzj6u52u30Kp6M/trliBMCMKTyK833zpbD+pXdCLuTusPj697FH4R/5mcr' crossorigin='anonymous'>")
        output.append("</head>")
        output.append("<body>")
        output.append("<div class='container'>")
        # write identifier as heading
        identifier = self._metadata.get("identifier", "").strip()
        if len(identifier) > 0:
            output.append("<h3>")
            if (identifier.startswith("http")):
                output.append(f"<a target='_blank' rel='noopener noreferrer' href='{identifier}'>{escape(identifier)}</a>")
            else:
                output.append(f"{escape(identifier)}")
            output.append("</h3>")

        if(include_metadata): 
            output.append("<details>")
            output.append(f"<summary class='metadata'>Metadata</summary>")
            output.append(self.metadata_to_html())
            output.append("</details>")

        # write displacy HTML rendering of doc text as paragraph with highlighted spans 
        if(include_doctext):
            output.append("<details open>")
            output.append(f"<summary class='doctext'>Text ({len(self.doctext)} characters)</summary>")
            output.append(f"<p>{self.doctext_to_html()}</p>")
            output.append("</details>")

        # write tokens
        if(include_tokens):
            output.append("<details>")
            output.append(f"<summary class='tokens'>Tokens ({len(self.tokens)})</summary>")
            output.append(self.tokens_to_html())
            output.append("</details>")

        # write spans
        if(include_spans):
            output.append("<details>")
            output.append(f"<summary class='spans'>Spans ({len(self.spans)})</summary>")
            output.append(self.spans_to_html())
            output.append("</details>")

        if(include_label_counts):
            output.append("<details>")
            output.append(f"<summary class='spans'>Label Counts ({len(self.label_counts)})</summary>")
            output.append(self.label_counts_to_html())
            output.append("</details>")

        # write span counts
        if(include_span_scores):
            output.append("<details>")
            output.append(f"<summary class='span-counts'>Span Counts ({len(self.span_scores)})</summary>")
            output.append(self.span_scores_to_html())
            output.append("</details>")
        
        # write span pairs
        if(include_span_pairs):
            output.append("<details>")
            output.append(f"<summary class='span-pairs'>Span Pairs ({len(self.span_pairs)})</summary>")
            output.append(self.span_pairs_to_html(self.span_pairs))
            output.append("</details>")

        # write negated pairs - this might not work now?? retest..
        if(include_negated_pairs):
            output.append("<details>")
            output.append(f"<summary class='span-pairs'>Negated Pairs ({len(self.negated_pairs)})</summary>")
            output.append(self.span_pairs_to_html(self.negated_pairs))
            output.append("</details>")

        # write footer tags
        output.append("</div>")  # close container
        output.append("</body>")
        output.append("</html>")

        # finally join and return all
        return f"\n".join(output)


    @run_timed
    def report_to_json(
        self, 
        include_metadata: bool = True,
        include_doctext: bool = True,        
        include_tokens: bool = True,
        include_label_counts: bool = True,
        include_spans: bool = True,        
        include_span_scores: bool = True,
        include_span_pairs: bool = True,
        include_negated_pairs: bool = False) -> str:
        output = {
            "metadata": self.metadata if include_metadata else {},
            "text": self.doctext if include_doctext else "",
            "tokens": self.tokens_to_list() if include_tokens else [],
            "label_counts": self.label_counts if include_label_counts else [],
            "spans": self.spans_to_list() if include_spans else [],
            "span_scores": self.span_scores if include_span_scores else [],
            "span_pairs": self.span_pairs_to_list(self.span_pairs) if include_span_pairs else [],
            "negated_pairs": self.span_pairs_to_list(self.negated_pairs) if include_negated_pairs else []
        }
        return json.dumps(output, default=str)


    @run_timed
    def report_to_text(
        self, 
        include_metadata: bool = True,
        include_doctext: bool = True,        
        include_tokens: bool = False,
        include_label_counts: bool = True,
        include_spans: bool = False,        
        include_span_scores: bool = True,
        include_span_pairs: bool = True,
        include_negated_pairs: bool = False
        ) -> str:
        output = []
        output.append(f"identifier: {self._metadata.get('identifier', '')}")
        if include_metadata:
            output.append(f"metadata:\n{self.metadata_to_text()}")        
        if include_doctext:
            output.append(f"text:\n{self.doctext}")
        if include_tokens:
            output.append(f"tokens:\n{self.tokens_to_text()}")
        if include_label_counts:
            output.append(f"label_counts:\n{self.label_counts_to_text()}")    
        if include_spans:
            output.append(f"spans:\n{self.spans_to_text()}")
        if include_span_scores:
            output.append(f"span counts:\n{self.span_scores_to_text()}")
        if include_span_pairs:
            output.append(f"span pairs:\n{self.span_pairs_to_text(self.span_pairs)}")
        if include_negated_pairs:
            output.append(f"negated pairs:\n{self.span_pairs_to_text(self.negated_pairs)}")
        return f"\n{'-' * 80}\n".join(output)

    
    @staticmethod
    def span_pairs_to_df(pairs: list[SpanPair] = []) -> DataFrame:
        df = DataFrame([{
            "span1_id": pair.span1.id_,
            "span1_label": pair.span1.label_,
            "span1_text": pair.span1.text,
            "rel_op": pair.rel_op,
            "span2_id": pair.span2.id_,
            "span2_label": pair.span2.label_,
            "span2_text": pair.span2.text,
            "score": pair.score
        } for pair in pairs])        
           
        return df

    @staticmethod
    def span_pairs_to_csv(pairs: list[SpanPair] = [], sep=",") -> str:
        df = DocSummary.span_pairs_to_df(pairs)
        return df.to_csv(sep=sep)


    @staticmethod
    def span_pairs_to_list(pairs: list[SpanPair] = []) -> list:
        df = DocSummary.span_pairs_to_df(pairs)
        return df.to_dict(orient="records")


    @staticmethod
    def span_pairs_to_html(pairs: list[SpanPair] = []) -> str:
        df = DocSummary.span_pairs_to_df(pairs)
        if df.empty:
            return ""        
        
        # create html links from id and text
        df["span1"] = df.apply(lambda row: DocSummary._make_link(row["span1_id"], row["span1_text"]), axis=1)
        df["span2"] = df.apply(lambda row: DocSummary._make_link(row["span2_id"], row["span2_text"]), axis=1)
        
        html = df.to_html(
            columns=["span1", "span1_label", "rel_op", "span2", "span2_label", "score"],
            border=0,
            index=False, 
            render_links=True, 
            escape=False,
            na_rep='',
            classes=['table', 'table-sm', 'table-striped', 'table-light']
        )
        return html  


    @staticmethod
    def span_pairs_to_json(pairs: list[SpanPair] = []) -> str:
        df = DocSummary.span_pairs_to_df(pairs)
        return df.to_json(orient="records")


    @staticmethod
    def span_pairs_to_text(pairs: list[SpanPair] = []) -> str:
        df = DocSummary.span_pairs_to_df(pairs)
        pd.set_option('display.max_colwidth', None)
        return(df.to_string(index=False)) if len(df) > 0 else "NO RECORDS" 


# test the DocSummary class
if __name__ == "__main__":
    
    # example test
    test_text = """This collection comprises Roman site data(reports, images, spreadsheets, GIS data and site records) from two phases of archaeological evaluation undertaken by Oxford Archaeology in June 2018 (SAWR18) and February 2021 (SAWR21) at West Road, Sawbridgeworth, Hertfordshire. SAWR18 In June 2018, Oxford Archaeology were commissioned by Taylor Wimpey to undertake an archaeological evaluation on the site of a proposed housing development to the north of West Road, Sawbridgeworth(TL 47842 15448). A programme of 19 trenches was undertaken to ground truth the results of a geophysical survey and to assess the archaeological potential of the site. The evaluation confirmed the presence of archaeological remains in areas identified on the geophysics. Parts of a NW-SE‐aligned trackway were found in Trenches 1 and 2. Field boundaries identified by geophysics(also present on the 1839 tithe map) were found in Trenches 5 and 7, towards the south of the site, and in Trenches 12 and 16, in the centre of the site. Geophysical anomalies identified in the northern part of the site were investigated and identified as geological. The archaeology is consistent with the geophysical survey results and it is likely that much of it has been truncated by modern agricultural activity. SAWR21 Oxford Archaeology carried out an archaeological evaluation on the site of proposed residential development north of West Road, Sawbridgeworth, Hertfordshire, in February 2021. The fieldwork was commissioned by Taylor Wimpey as a condition of planning permission. Preceding geophysical survey of the c 5.7ha development site was undertaken in 2016 and identified a concentration of linear and curvilinear anomalies in the north-east corner of the site and two areas of several broadly NW-SE aligned anomalies in the southern half of the site. Subsequent trial trench evaluation, comprising the investigation of 19 trenches, was undertaken by Oxford Archaeology in 2018, targeted upon the geophysical survey results. The evaluation revealed a small number of ditches in the centre and south of the site, correlating with the geophysical anomalies. Although generally undated, the ditches were suggestive of a trackway and associated enclosure/field boundaries. Other ditches encountered on site correlated with post-medieval field boundaries depicted on 19th century mapping. Given the results of the 2018 evaluation, in conjunction with those of the 2018 investigations at nearby Chalk's Farm, which uncovered the remains of Late Bronze Age-early Iron Age and early Roman settlement and agricultural activity, it was deemed necessary to undertake a further phase of evaluation at the site. Four additional trenches were excavated in the southern half of the site to further investigate the previously revealed ditches. The continuations of the trackway ditches were revealed in the centre of the site, with remnants of a metalled surface also identified. Adjacent ditches may demonstrate the maintenance and modification of the trackway or perhaps associated enclosure/field boundaries. Artefactual dating evidence recovered from these ditches was limited and of mixed date, comprising small pottery sherds of late Bronze Age- Early Iron Age date and fragments of Roman ceramic building material. It is probable that these remains provide evidence of outlying agricultural activity associated with the later prehistoric and early Roman settlement evidence at Chalk's Farm. A further undated ditch and a parallel early Roman ditch were revealed in the south of the site, suggestive of additional land divisions, probably agricultural features. A post-medieval field boundary ditch and modern land drains are demonstrative of agricultural use of the landscape during these periods."""
    nlp = spacy.load("en_core_web_sm")   #nlp = spacy.load("en_core_web_sm", disable=['ner']) 
    nlp.add_pipe("fish_monument_types_ruler", last=True)
    doc = nlp(test_text)
    summary = DocSummary(doc)
    data = doc.to_json() #["spans"] = doc.spans
    
    with open("../data/test_serialisation.json", "w") as outfile:
        json.dump(data, outfile)
    #print("\nTokens:\n" + summary.tokens_to_text())
    #print("\nSpans:\n" + summary.spans_to_text())    