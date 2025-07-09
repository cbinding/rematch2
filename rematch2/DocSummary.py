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
    .doctext, .tokens, .spans, .spancounts, .labels, .labelcounts, .spanpairs 
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
from spacy.tokens import Doc, Span, Token, SpanGroup
from spacy import displacy
from SpanPair import SpanPair
from .SpanPairs import SpanPairs
from .Decorators import run_timed
from .Util import DEFAULT_SPANS_KEY


class DocSummary:

    def __init__(
            self, 
            doc: Doc, 
            spans_key: str=DEFAULT_SPANS_KEY, 
            metadata: dict[str, str] = {}            
        ):
        self._doc = doc
        self._spans_key = spans_key.strip()
        self._metadata = metadata

        # copy any entities to spans so they can be reported and displayed
        # in the same way as all other spans identified
        for ent in doc.ents: doc.spans[spans_key].append(ent)            

        # calculate and attach concept frequency (similar to term frequency)
        self._calculate_concept_frequency() 


    def _calculate_concept_frequency(self):
        spans = self._doc.spans.get(self._spans_key, [])
        label_count = {}
        id_count = {}
        for span in spans:
            # increment counter of spans for this label 
            # (number of concepts of this type in the document)
            label = (span.label_ or "nothing")
            if len(label) > 0:
                if label not in label_count:
                    label_count[label] = 1
                else:
                    label_count[label] += 1
            # increment counter of spans for this id 
            # (number of times this concept appears in the document)
            id = (span.id_ or "nothing")
            if len(id) > 0:
                if id not in id_count:
                    id_count[id] = 1
                else:
                    id_count[id] += 1
        
        # casting to floats to ensure the result is float; 
        # default denominator of 1 prevents divide by zero errors
        cf_value = lambda span: float(id_count.get(span.id_, 0)) / float(label_count.get(span.label_, 1))
        Span.set_extension("cf_value", getter = cf_value, force=True)
        

    @property
    def metadata(self) -> dict[str,str]: 
        return self._metadata
    

    @property
    def doctext(self) -> str:
      return self._doc.text
    

    @property
    def spans(self) -> list[Span]:
      return self._doc.spans.get(self._spans_key, [])


    @property
    def tokens(self) -> list[Token]:
        return [t for t in self._doc]
    

    @cached_property
    def span_pairs(self) -> list[SpanPair]:
        pairs = DocSummary.get_span_pairs(self.spans)
        return pairs

    @cached_property
    def span_counts(self) -> list[SpanPairs]:
        counts = self.get_span_counts_by_id() 
        return counts


    @cached_property
    def label_counts(self) -> list:
        counts = self.get_span_counts_by_label()
        return counts


    def __str__(self):
        return self.doctext


    def __repr__(self):
        return self.__str__()

             
    @staticmethod
    def metadata_to_html(data: dict[str, str]) -> str:
        html = []
        html.append("<ul>")
        for key, val in data.items():
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


    @staticmethod
    def metadata_to_json(data: dict[str, str]) -> str:
        return json.dumps(data)


    @staticmethod
    def metadata_to_text(data: dict[str, str]) -> str:
        text = []
        for key, val in data.items():
            text.append(f"* {key}: {str(val)}")
            
        return f"\n".join(text)

    
    @staticmethod
    def doctext_to_text(doc: Doc) -> str: return doc.text

    @staticmethod
    def doctext_to_html(
        doc: Doc,
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
                #"DATEPREFIX": "lightgray",
                #"DATESUFFIX": "lightgray",
                #"DATESEPARATOR": "lightgray",
                #"ORDINAL": "lightgray",
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
                "FISH_MATERIAL": "antiquewhite",
                "FISH_EVENTTYPE": "coral"
            } 
        }
    
        # create temp subset (as options don't specify what to show/exclude)
        doc.spans["temp_subset"] = list(filter(lambda span: span.label_ not in exclude, doc.spans))

        # create HTML string rendering the document text with highlighted spans       
        html = displacy.render(
            docs = doc,
            style = "span", 
            page = False, 
            minify = False, 
            jupyter = False, 
            options = default_options | options | {"spans_key": "temp_subset"} # shallow merging
        )

        # remove the temp subset and return the HTML rendered string
        del doc.spans["temp_subset"]
        return html


    @run_timed
    def report(self, format: str="text") -> str: 
        match format.strip().lower():  
            case "html": return self.report_to_html()
            case "json": return self.report_to_json()
            case "text": return self.report_to_text()
            case _: return self.report_to_text()        

    
           
    @staticmethod
    def spans_to_df(spans: list[Span]) -> DataFrame: 
        return DataFrame([{
            "start": span.start_char,
            "end": span.end_char,
            "token_start": span.start,
            "token_end": span.end - 1,            
            "label": span.label_,
            "id": span.id_,
            "text": span.text,
            "cf": span._.cf_value
            } for span in spans]).drop_duplicates()


    @staticmethod
    def spans_to_csv(spans: list[Span], sep=",") -> str:
        df = DocSummary.spans_to_df(spans)
        return df.to_csv(sep=sep)


    @staticmethod
    def spans_to_html(spans: list[Span]) -> str:
        df = DocSummary.spans_to_df(spans)
        return(df.to_html(index=False, border=True)) # renders html table


    @staticmethod
    def spans_to_html_list(spans: list[Span]) -> str:
        html = []
        html.append("<details>")
        html.append(f"<summary>Spans ({len(spans)})</summary>")
        html.append("<ul class='entities'>") 
        for span in spans:
            html.append("<li class='entity {label}'>({start}&#8594;{end}) [{label}] {id} \"{text}\"</li>".format(
                start = span.start_char, 
                end = span.end_char,
                label = span.label_,
                id = span.id_,
                text = span.text
            ))        
        html.append("</ul>") 
        html.append("</details>")
        return "\n".join(html) 


    @staticmethod
    def spans_to_json(spans: list[Span]) -> str:
        df = DocSummary.spans_to_df(spans)
        return df.to_json(orient="records")


    @staticmethod
    def spans_to_list(spans: list[Span]) -> list:
        df = DocSummary.spans_to_df(spans)
        return df.to_dict(orient="records")


    @staticmethod
    def spans_to_text(spans: list[Span]) -> str:
        df = DocSummary.spans_to_df(spans)
        pd.set_option('display.max_colwidth', None)
        return(df.to_string(index=False))


    @run_timed
    def get_span_pairs(self, 
        left_labels: list=["PERIOD", "YEARSPAN"], 
        right_labels: list=["FISH_OBJECT", "FISH_MONUMENT"], 
        #rel_ops: list=[ "<", ">", "<<", ">>", ".", ".*", ";", ";*" ]
        rel_ops: list=[ "<", ">", ".", ";" ]
        ) -> str|list:

        pairs = SpanPairs(doc=self._doc, rel_ops=rel_ops, left_labels=left_labels, right_labels=right_labels).pairs

        return pairs


    # count spans by id, return list [{id, label, text, count}, {id, label, text, count}, ...] 
    # returned in descending count order - note there is probably a more elegant way to do this 
    def get_span_counts_by_id(
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
        spans = self.spans()
        counts = {}
        #spans_count = len(list(filter(lambda s: s.label_ not in exclude, spans)))

        for span in spans:
            # exclude specified labels from summary counts
            if span.label_ in exclude:
                continue

            # get suitable identifier to aggregate counts
            id=""
            if span.id_:
                id = span.id_
            elif span.ent_id_:
                id = span.ent_id_
            elif span.lemma_:
                id = span.lemma_
            elif span.text:
                id = span.text
            else:
                id = "other"
             
            # create a new record if not encountered before, or increment the existing count
            if id not in counts:
                counts[id] = { "id": id, "label": span.label_, "text": span.lemma_, "count": 1, "cf": span._.cf_value } 
            else:
                counts[id]["count"] += 1                        
        
        # return as list sorted by ascending count
        return sorted(list(counts.values()), key=lambda x: x.get("count", 0), reverse=True)


    @staticmethod
    def span_counts_to_df(counts: list) -> DataFrame: 
        return DataFrame([{
            "id": item.get("id", ""),
            "label": item.get("label", ""),
            "text": item.get("text", ""),
            "count": int(item.get("count", 0)),
            "cf": float(item.get("cf", 0))
            } for item in counts]) 


    @staticmethod
    def span_counts_to_csv(counts: list, sep: str=",") -> str:
        df = DocSummary.span_counts_to_df(counts)
        return df.to_csv(sep=sep)


    @staticmethod
    def span_counts_to_html(counts: list) -> str:
        df = DocSummary.span_counts_to_df(counts)
        return(df.to_html(index=False, border=0)) # renders html table


    # table rendering from find_pairs.py
    @staticmethod
    def span_counts_to_html_table(counts: list) -> str:
        html = []        
        if len(counts) == 0:
            html.append("<p>NONE FOUND</p>")
        else:
            html.append("<table><tbody>")
            for item in counts:
                html.append("<tr>")
                html.append("<td style='text-align:right; vertical-align: middle;'>")
                html.append(f"<div class='entity {escape(item['label'].lower())}'>")
                if(item['id'].startswith("http")):
                    html.append(f"<a target='_blank' rel='noopener noreferrer' href='{item['id']}'>{escape(item['text'])}</a>")
                else:
                    html.append(f"{escape(item['text'])}")
                html.append("</div>")
                html.append("</td>")
                html.append(f"<td>({item['count']})</td>")
                html.append(f"<td>({item['cf']})</td>")
                html.append("</tr>")
            html.append("</tbody></table>")
        return "\n".join(html)


    @staticmethod
    def span_counts_to_html_list(counts: list) -> str:
        html = []
        html.append("<ul class='entities'>")
        for item in counts:
            html.append(f"<li class='entity {escape(item['label'].lower())}'>")
            if(item['id'].startswith("http")):
                html.append(f"<a target='_blank' rel='noopener noreferrer' href='{item['id']}'>{escape(item['text'])}</a>")
            else:
                html.append(f"{escape(item['text'])}")
            html.append(f" ({item['count']}) ({item['cf']})")
            html.append("</li>")
        html.append("</ul>")
        return "\n".join(html)


    @staticmethod
    def span_counts_to_json(counts: list) -> str:
        df = DocSummary.span_counts_to_df(counts)
        return df.to_json(orient="records")


    @staticmethod
    def span_counts_to_text(counts: list) -> str:
        df = DocSummary.span_counts_to_df(counts)
        pd.set_option('display.max_colwidth', None)
        return(df.to_string(index=False))


    @staticmethod
    def span_counts_to_text_custom(counts: list) -> str:
        lines = []
        for item in counts:                    
            lines.append("[{label}] {id:<60} {text:>20} ({count}) ({cf})".format(
                id = item.get("id", ""),                
                label = item.get("label", ""),
                text = item.get("text", ""),
                count = int(item.get("count", 0)),
                cf = float(item.get("cf", 0))
                )
            )
        return "\n".join(lines) 


    # count spans by label, return list [{label, count}, {label, count}, ...] 
    # returned in descending count order
    @staticmethod
    def get_span_counts_by_label(
        spans: list[Span] = [],
        exclude: list = [
            "NEGATION", 
            "DATEPREFIX", 
            "DATESEPARATOR", 
            "DATESUFFIX", 
            "ORDINAL", 
            "MONTHNAME", 
            "SEASONNAME"
        ]) -> list:
         
        counts = {}

        for span in spans:
            label = span.label_
            # exclude specified labels from summary counts
            if label in exclude:
                continue            
            
            # create a new record if not encountered before, or increment the count
            if label not in counts:
                counts[label] = { "label": label, "count": 1 } 
            else:
                counts[label]["count"] += 1            
        
        # return as list sorted by ascending count
        return sorted(list(counts.values()), key=lambda x: x.get("count", 0), reverse=True)

    @staticmethod
    def label_counts_to_df(counts: list) -> DataFrame: 
        # convert to DataFrame, casting count to int
        # (in case it is a float, e.g. if cf_value was used)
        return DataFrame([{
            "label": item.get("label", ""),
            "count": int(item.get("count", 0))
            } for item in counts]) 


    @staticmethod
    def label_counts_to_csv(counts: list, sep: str=",") -> str:
        df = DocSummary.labelcounts_to_df(counts)
        return df.to_csv(sep=sep)


    @staticmethod
    def label_counts_to_html(counts: list) -> str:
        df = DocSummary.labelcounts_to_df(counts)
        return(df.to_html(index=False, border=0)) # renders html table
    
    
    @staticmethod
    def label_counts_to_html_list(counts: list) -> str:
        html = []
        html.append("<details>")
        html.append(f"<summary>Labels ({len(counts)})</summary>")
        html.append("<ul class='entities'>") 
        for item in counts:
            html.append("<li><div class='entity {label}'>&nbsp;</div>({count})</li>".format(
                label = item.get("label", "").lower(),
                count = item.get("count", 0)
            ))        
        html.append("</ul>") 
        html.append("</details>")
        return "\n".join(html) 

    
    @staticmethod
    def label_counts_to_html_table(counts: list) -> str:
        html = []        
        if len(counts) == 0:
            html.append("<p>NONE FOUND</p>")
        else:
            html.append("<table><tbody>")
            for item in counts:
                html.append("<tr>")
                html.append("<td style='text-align:right; vertical-align: middle;'>")
                html.append(f"<div class='entity {escape(item['label'].lower())}'>")
                html.append(f"{escape(item['label'])}")
                html.append("</div>")
                html.append("</td>")
                html.append(f"<td>({item['count']})</td>")
                html.append("</tr>")
            html.append("</tbody></table>")
        return "\n".join(html)

   
    @staticmethod
    def label_counts_to_json(counts: list) -> str:
        df = DocSummary.label_counts_to_df(counts)
        return df.to_json(orient="records")

    
    @staticmethod
    def label_counts_to_text(counts: list) -> str:
        df = DocSummary.label_counts_to_df(counts)
        pd.set_option('display.max_colwidth', None)
        return(df.to_string(index=False))

    
    @staticmethod
    def label_counts_to_text_custom(counts: list) -> str:
        lines = []
        for item in counts:                    
            lines.append("[{label}] ({count})".format(
                label = item.get("label", ""),
                count = int(item.get("count", 0))
            ))
        return "\n".join(lines) 


    @staticmethod
    def tokens_to_df(toks: list[Token]) -> DataFrame: 
        if len(toks) == 0:
            return DataFrame(columns=["index", "start", "end", "pos", "text", "lemma"])
        else:
            return DataFrame([{
                "index": tok.i,
                "start": tok.idx + 1,
                "end": tok.idx + len(tok.text),
                "pos": tok.pos_,
                "text": tok.text,
                "lemma": tok.lemma_,
                } for tok in toks])  
    

    @staticmethod
    def tokens_to_csv(toks: list[Token], sep: str=",") -> str:
        df = DocSummary.tokens_to_df(toks)
        return df.to_csv(sep=sep)
            

    @staticmethod
    def tokens_to_html(toks: list[Token]) -> str:
        df = DocSummary.tokens_to_df(toks)
        return df.to_html(index=False, border=0) # renders html table


    @staticmethod
    def tokens_to_list(toks: list[Token]) -> list:
        df = DocSummary.tokens_to_df(toks)
        return df.to_dict(orient="records")

    
    @staticmethod
    def tokens_to_html_list(toks: list[Token]) -> str:
        html = []
        html.append("<ul class='tokens'>")
        for tok in toks:
            html.append("<li class='token'>[{index}] ({start}&#8594;{end}) pos=\"{pos:<3}\" text=\"{text}\" lemma=\"{lemma}\"</li>".format(
                index = tok.i,
                start = tok.idx + 1,
                end = tok.idx + len(tok.text),
                pos = tok.pos_,
                text = escape(tok.text),
                lemma = escape(tok.lemma_)         
            ))
        html.append("</ul>")
        return "\n".join(html)   


    @staticmethod
    def tokens_to_json(toks: list[Token]) -> str:
        df = DocSummary.tokens_to_df(toks)
        return df.to_json(orient="records")

    
    @staticmethod
    def tokens_to_text(toks: list[Token]) -> str:
        df = DocSummary.tokens_to_df(toks)
        pd.set_option('display.max_colwidth', None)
        return(df.to_string(index=False))

    
    @staticmethod
    def tokens_to_text_custom(toks: list[Token]) -> str:
        lines = ["[{index}] ({start}->{end}) {pos:<4} \"{text}\"".format(
            index = tok.i,
            start = tok.idx + 1,
            end = tok.idx + len(tok.text),
            pos = tok.pos_,
            text = tok.text
            ) for tok in toks]
        return "\n".join(lines)

   
    @run_timed
    def report_to_html(self, include_tokens: bool = False) -> str:
        output = []

        # write header tags
        output.append("<!DOCTYPE html>")
        output.append("<html>")
        output.append("<head>")
        file_path = os.path.join(Path(__file__).parent, "DocSummary.css")
        with open(file_path, 'r', encoding='utf8') as css_file:
            css_text = css_file.read()
            output.append(f'<style>{css_text}</style>')    
    
        output.append("</head>")
        output.append("<body>")

        # write identifier as heading
        identifier = self._metadata.get("identifier", "").strip()
        if len(identifier) > 0:
            output.append("<h3>")        
            if(identifier.startswith("http")):
                output.append(f"<a target='_blank' rel='noopener noreferrer' href='{identifier}'>{escape(identifier)}</a>")
            else:
                output.append(f"{escape(identifier)}")
            output.append("</h3>")

        # write metadata   
        output.append("<details>")
        output.append(f"<summary>Metadata</summary>")
        output.append(DocSummary.metadata_to_html(self._metadata))
        output.append("</details>")

        # write displacy HTML rendering of doc text as paragraph with highlighted spans 
        text = self.doctext()        
        output.append("<details open>")
        output.append(f"<summary>Text ({len(text)} characters)</summary>")
        output.append(f"<p>{DocSummary.doctext_to_html(self._doc)}</p>")
        output.append("</details>")

        # write tokens
        if(include_tokens):
            output.append("<details>")
            output.append(f"<summary>Tokens ({len(DocSummary.tokens_to_list(self.tokens))})</summary>")
            output.append(DocSummary.tokens_to_html_list(self.tokens))
            output.append("</details>")

        # write span counts
        output.append("<details>")
        output.append(f"<summary>Span Counts ({len(self.span_counts)})</summary>")
        output.append(DocSummary.spancounts_to_html_table(self.span_counts))
        output.append("</details>")

        # write span pairs
        output.append("<details>")
        output.append(f"<summary>Span Pairs</summary>")
        output.append(DocSummary.spanpairs_to_html(self.span_pairs))
        output.append("</details>")

        # write negated pairs - this might not work now?? retest..
        output.append("<details>")
        output.append(f"<summary>Negated Pairs</summary>")
        pairs = self.span_pairs(
            format="htmlt", 
            left_labels=["NEGATION"], 
            right_labels=["YEARSPAN", "PERIOD", "FISH_OBJECT", "FISH_MONUMENT"]
        )
        output.append(pairs)
        output.append("</details>")

        # write footer tags
        output.append("</body>")
        output.append("</html>")

        # finally join and return all
        return f"\n".join(output)


    @run_timed
    def report_to_json(self, include_tokens: bool=False):
        output = {
            "metadata": self.metadata,
            "text": self.doctext,
            "tokens": self.tokens if include_tokens else [],
            "spans": self.spans,
            "span_counts": self.span_counts,
            "span_pairs": self.span_pairs,
        }
        return json.dumps(output, default=str)


    @run_timed
    def report_to_text(self, include_tokens: bool=False) -> str:
        output = []
        output.append(f"metadata:\n{DocSummary.meta_to_text(self.metadata)}")        
        output.append(f"text:\n{self.doctext}")
        if include_tokens:
            output.append(f"tokens:\n{DocSummary.tokens_to_text(self.tokens)}")
        output.append(f"spans:\n{DocSummary.spans_to_text(self.spans)}")        
        output.append(f"span counts:\n{DocSummary.span_counts_to_text(self.span_counts)}")
        output.append(f"span pairs:\n{DocSummary.span_pairs_to_text(self.span_pairs)}")
        return f"\n{'-' * 80}\n".join(output)

    
    @staticmethod
    def span_pairs_to_df(pairs: list = []) -> DataFrame:
        return DataFrame([{
            "span1_id": pair.span1.id_,
            "span1_label": pair.span1.label_,
            "span1_text": pair.span1.text,
            "rel_op": pair.rel_op,
            "span2_id": pair.span2.id_,
            "span2_label": pair.span2.label_,
            "span2_text": pair.span2.text,
            "score": pair.score
        } for pair in pairs])
        

    @staticmethod
    def span_pairs_to_csv(pairs: list = [], sep=",") -> str:
        df = DocSummary.span_pairs_to_df(pairs)
        return df.to_csv(sep=sep)


    @staticmethod
    def span_pairs_to_list(pairs: list = []) -> list:
        df = DocSummary.span_pairs_to_df(pairs)
        return df.to_dict(orient="records")


    @staticmethod
    def span_pairs_to_html(pairs: list = []) -> str:
        df = DocSummary.span_pairs_to_df(pairs)
        return(df.to_html(index=False, border=0)) # renders html table

    @staticmethod
    def span_pairs_to_html(pairs: list = []) -> str:
        return "<p>NOT IMPLEMENTED YET</p>"


    # custom table render from find_pairs.py 
    @staticmethod
    def span_pairs_to_html_table(pairs: list = []) -> str:
        html = []

        def _span_to_html(span) -> str:
            lines = []
            lines.append(f"<div class='entity {escape(span.label_.lower())}'>")
            if(span.id_.startswith("http")):
                lines.append(f"<a target='_blank' rel='noopener noreferrer' href='{span.id_}'>{escape(span.text)}</a>")
            else:
                lines.append(f"{escape(span.text)}")
            lines.append("</div>")
            return "\n".join(lines)


        if len(pairs) == 0:
            html.append("<p>NONE FOUND</p>")
        else:            
            html.append("<table><tbody>")
            for pair in pairs:
                html.append("<tr>")
                html.append(f"<td style='text-align:right; vertical-align: middle'>{_span_to_html(pair.span1)}</td>")                
                html.append(f"<td style='text-align:center; vertical-align: middle'>{escape(pair.rel_op)}</td>")
                html.append(f"<td style='text-align:right; vertical-align: middle'>{_span_to_html(pair.span2)}</td>")
                html.append(f"<td>({pair.score})</td>")
                html.append("</tr>")
            html.append("</tbody></table>")
        return "\n".join(html)


    @staticmethod
    def span_pairs_to_json(pairs: list = []) -> str:
        df = DocSummary.span_pairs_to_df(pairs)
        return df.to_json(orient="records")


    @staticmethod
    def span_pairs_to_text(pairs: list = []) -> str:
        df = DocSummary.span_pairs_to_df(pairs)
        pd.set_option('display.max_colwidth', None)
        return(df.to_string(index=False))


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