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
Example   : html = DocSummary(doc).spans("html")
    .doctext, .tokens, .spans, .spancounts, .labels, .labelcounts, .spanpairs 
License   : https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History
14/03/2024 CFB consolidated and centralized code from other scripts
=============================================================================
"""
from html import escape
import json
import os
from pathlib import Path
import pandas as pd
from html import escape # for writing escaped HTML
from pandas import DataFrame
from spacy.tokens import Doc, Span
from spacy import displacy

if __package__ is None or __package__ == '':
    # uses current directory visibility
    from SpanPairs import SpanPairs
else:
    # uses current package visibility
    from .SpanPairs import SpanPairs


class DocSummary:

    def __init__(self, doc: Doc, spans_key: str="rematch", metadata: dict = {}):
        self._doc = doc
        self._spans_key = spans_key.strip()
        self._metadata = metadata

        # copy any PLACE entities to spans so they can be reported and displayed
        # in the same way as all other slans identified
        for ent in filter(lambda x: x.label == "LOC", doc.ents):
            doc.spans[spans_key].append(ent)
            print(ent.text)

        # calculate and attach concept frequency (similar to term frequency)
        self._calculate_concept_frequency()
    

    def __str__(self):
        return self.doctext()


    def __repr__(self):
        return self.__str__()

    
    def meta(self, format: str="text") -> str:         
        match format.strip().lower(): 
            case "html": return self._meta_to_html(self._metadata)
            case "json": return self._meta_to_json(self._metadata)
            case "text": return self._meta_to_text(self._metadata)
            case "dict": return self._metadata
            case _: return self._metadata   


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
        

    def doctext(self, format: str="text") -> str: 
        match format.strip().lower():  
            case "html": return self._doctext_to_html(self._doc, spans_key=self._spans_key)
            case _: return self._doc.text


    def report(self, format: str="text") -> str: 
        match format.strip().lower():  
            case "html": return self._report_to_html()
            case "json": return self._report_to_json()
            case "text": return self._report_to_text()
            case _: return self._report_to_text()        

    
    def spans(self, format: str="text", label="") -> str|list:
        spans = self._doc.spans.get(self._spans_key, [])
        if(label != ""):
            spans = filter(lambda span: span.label_ == label, spans)



        match format.strip().lower():
            case "csv": return self._spans_to_csv(spans)
            case "html": return self._spans_to_html(spans)
            case "htmll": return self._spans_to_html_list(spans)
            case "json": return self._spans_to_json(spans)
            case "list": return self._spans_to_list(spans)
            case "text": return self._spans_to_text(spans)
            case _: return spans


    def spanpairs(self, 
        format: str="text", 
        left_labels: list=["PERIOD", "YEARSPAN"], 
        right_labels: list=["FISH_OBJECT", "FISH_MONUMENT"], 
        rel_ops: list=[ "<", ">", "<<", ">>", ".", ";" ]
        ) -> str|list:

        pairs = SpanPairs(doc=self._doc, rel_ops=rel_ops, left_labels=left_labels, right_labels=right_labels).pairs

        match format.strip().lower():
            case "csv": return self._spanpairs_to_csv(pairs)
            case "html": return self._spanpairs_to_html(pairs)   # render as a table
            case "htmll": return self._spanpairs_to_html_list(pairs) # render as a list
            case "htmlt": return self._spanpairs_to_html_table(pairs) # rendering from find_pairs.py
            case "json": return self._spanpairs_to_json(pairs)
            case "text": return self._spanpairs_to_text(pairs)
            case "list": return self._spanpairs_to_list(pairs)
            case _: return pairs

    
    def spancounts(self, format: str="text") -> str|list:
        spans = self.spans(format="default")
        counts = self._get_span_counts_by_id(spans)
        match format.strip().lower():
            case "csv": return self._spancounts_to_csv(counts)
            case "html": return self._spancounts_to_html(counts) # render as a table
            case "htmll": return self._spancounts_to_html_list(counts) # render as a list
            case "htmlt": return self._spancounts_to_html_table(counts) # rendering from find_pairs.py
            case "json": return self._spancounts_to_json(counts)
            case "text": return self._spancounts_to_text(counts)
            case "list": return counts
            case _: return counts


    def labelcounts(self, format: str="text") -> str|list:
        spans = self.spans(format="default")
        counts = self._get_span_counts_by_label(spans)
        match format.strip().lower():
            case "csv": return self._labelcounts_to_csv(counts)
            case "html": return self._labelcounts_to_html(counts) # render as a table
            case "htmll": return self._labelcounts_to_html_list(counts) # render as a list
            case "htmlt": return self._labelcounts_to_html_table(counts)
            case "json": return self._labelcounts_to_json(counts)
            case "text": return self._labelcounts_to_text(counts)
            case "list": return counts
            case _: return counts


    def tokens(self, format: str="text") -> str|list:
        toks = self._doc
        match format.strip().lower():
            case "csv": return self._tokens_to_csv(toks)
            case "html": return self._tokens_to_html(toks)  # render as a table
            case "htmll": return self._tokens_to_html_list(toks) # render as a list
            case "json": return self._tokens_to_json(toks)            
            case "text": return self._tokens_to_text(toks)
            case "list": return self._tokens_to_list(toks)
            case _: return toks


    @staticmethod
    def _meta_to_html(data: dict) -> str:
        html = []
        html.append("<ul>")
        for key, val in data.items():
            html.append(f"<li>")
            html.append(f"<strong>{escape(key)}:</strong>")
            if isinstance(val, dict):
                html.append(DocSummary._meta_to_html(val))
            elif isinstance(val, str):
                html.append(escape(val))               
            else:
                html.append(str(val))
            html.append('</li>')            
        html.append("</ul>")

        # finally join and return
        return f"\n".join(html)


    @staticmethod
    def _meta_to_json(data: dict) -> str:
        return json.dumps(data)


    @staticmethod
    def _meta_to_text(data: dict) -> str:
        text = []
        for key, val in data.items():
            if isinstance(val, dict):
                text.append(f"* {key}:")
                text.append(DocSummary._meta_to_text(val))
            else:
                text.append(f"* {key}: {str(val)}")
            
        # finally join and return
        return f"\n".join(text)


    @staticmethod
    def _doctext_to_html(
        doc: Doc, 
        spans_key: str="rematch", 
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
            "spans_key": "rematch",
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
        #opts = options | default_options #if options == None else options 

        # create temp subset (as options don't specify what to show/exclude)
        all_spans = doc.spans.get(spans_key, [])
        doc.spans["temp_subset"] = list(filter(lambda span: span.label_ not in exclude, all_spans)) 

        # create HTML string rendering the document text with highlighted spans       
        html = displacy.render(
            docs = doc, 
            style = "span", 
            page = False, 
            minify = False, 
            jupyter = False, 
            options = default_options | options | {"spans_key": "temp_subset"} #shallow merging
        )

        # remove the temp subset and return the HTML rendering string
        del doc.spans["temp_subset"]
        return html
   

    def _report_to_html(self) -> str:
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
        output.append(self.meta(format='html'))
        output.append("</details>")

        # write displacy HTML rendering of doc text as paragraph with highlighted spans 
        text = self.doctext(format="text")        
        output.append("<details open>")
        output.append(f"<summary>Text ({len(text)} characters)</summary>")
        output.append(f"<p>{self.doctext(format='html')}</p>")
        output.append("</details>")

        # write tokens
        output.append("<details>")
        output.append(f"<summary>Tokens ({len(self.tokens(format='list'))})</summary>")        
        output.append(self.tokens(format="htmll"))
        output.append("</details>")

        # write span counts
        output.append("<details>")
        output.append(f"<summary>Span Counts ({len(self.spancounts(format='list'))})</summary>")
        output.append(self.spancounts(format="htmlt"))
        output.append("</details>")

        # write span pairs
        output.append("<details>")
        output.append(f"<summary>Span Pairs</summary>")
        output.append(self.spanpairs(format="htmlt"))
        output.append("</details>")

        # write negated pairs
        output.append("<details>")
        output.append(f"<summary>Negated Pairs</summary>")
        pairs = self.spanpairs(
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


    def _report_to_json(self):
        output = {
            "meta": self.meta(format="dict"),
            "text": self.doctext(format="text"),
            "tokens": self.tokens(format="list"),            
            "spans": self.spans(format="list"),
            "spancounts": self.spancounts(format="list"),
            "spanpairs": self.spanpairs(format="list"),            
        }
        return json.dumps(output)


    def _report_to_text(self) -> str:
        output = []
        output.append(f"metadata:\n{self.meta(format='text')}")        
        output.append(f"text:\n{self.doctext()}")
        output.append(f"tokens:\n{self.tokens(format='text')}")
        output.append(f"spans:\n{self.spans(format='text')}")        
        output.append(f"span counts:\n{self.spancounts(format='text')}")
        output.append(f"span pairs:\n{self.spanpairs(format='text')}")        
        return f"\n{'-' * 80}\n".join(output)


    @staticmethod
    def _spanpairs_to_df(pairs: list = []) -> DataFrame:
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
    def _spanpairs_to_csv(pairs: list = [], sep=",") -> str:
        df = DocSummary._spanpairs_to_df(pairs)
        return df.to_csv(sep=sep)


    @staticmethod
    def _spanpairs_to_list(pairs: list = []) -> list:
        df = DocSummary._spanpairs_to_df(pairs)
        return df.to_dict(orient="records")


    @staticmethod
    def _spanpairs_to_html(pairs: list = []) -> str:
        df = DocSummary._spanpairs_to_df(pairs)
        return(df.to_html(index=False, border=0)) # renders html table


    @staticmethod
    def _spanpairs_to_htmll(pairs: list = []) -> str:
        pass


    # custom table render from find_pairs.py 
    @staticmethod
    def _spanpairs_to_html_table(pairs: list = []) -> str:
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
    def _spanpairs_to_json(pairs: list = []) -> str:
        df = DocSummary._spanpairs_to_df(pairs)
        return df.to_json(orient="records")


    @staticmethod
    def _spanpairs_to_text(pairs: list = []) -> str:
        df = DocSummary._spanpairs_to_df(pairs)
        pd.set_option('display.max_colwidth', None)
        return(df.to_string(index=False))


    @staticmethod
    def _spancounts_to_df(counts: list = []) -> DataFrame: 
        return DataFrame([{
            "id": item.get("id", ""),
            "label": item.get("label", ""),
            "text": item.get("text", ""),
            "count": int(item.get("count", 0)),
            "cf": float(item.get("cf", 0))
            } for item in counts]) 


    @staticmethod
    def _spancounts_to_csv(counts: list = [], sep: str=",") -> str:
        df = DocSummary._spancounts_to_df(counts)
        return df.to_csv(sep=sep)


    @staticmethod
    def _spancounts_to_html(counts: list = []) -> str:
        df = DocSummary._spancounts_to_df(counts)
        return(df.to_html(index=False, border=0)) # renders html table

    # table rendering from find_pairs.py
    @staticmethod
    def _spancounts_to_html_table(counts: list = []) -> str:
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
    def _spancounts_to_html_list(counts: list = []) -> str:
        pass


    @staticmethod
    def _spancounts_to_json(counts: list = []) -> str:
        df = DocSummary._spancounts_to_df(counts)
        return df.to_json(orient="records")


    @staticmethod
    def _spancounts_to_text(counts: list = []) -> str:
        df = DocSummary._spancounts_to_df(counts)
        pd.set_option('display.max_colwidth', None)
        return(df.to_string(index=False))


    @staticmethod
    def _spancounts_to_text_custom(counts: list = []) -> str:
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
    

    @staticmethod
    def _labelcounts_to_df(counts: list = []) -> DataFrame: 
        return DataFrame([{
            "label": item.get("label", ""),
            "count": int(item.get("count", 0))
            } for item in counts]) 


    @staticmethod
    def _labelcounts_to_csv(counts: list = [], sep: str=",") -> str:
        df = DocSummary._labelcounts_to_df(counts)
        return df.to_csv(sep=sep)


    @staticmethod
    def _labelcounts_to_html(counts: list = []) -> str:
        df = DocSummary._labelcounts_to_df(counts)
        return(df.to_html(index=False, border=0)) # renders html table
    

    @staticmethod
    def _labelcounts_to_html_list(counts: list = []) -> str:
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
    def _labelcounts_to_html_table(counts: list = []) -> str:
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
    def _labelcounts_to_json(counts: list = []) -> str:
        df = DocSummary._labelcounts_to_df(counts)
        return df.to_json(orient="records")


    @staticmethod
    def _labelcounts_to_text(counts: list = []) -> str:
        df = DocSummary._labelcounts_to_df(counts)
        pd.set_option('display.max_colwidth', None)
        return(df.to_string(index=False))


    @staticmethod
    def _labelcounts_to_text_custom(counts: list = []) -> str:
        lines = []
        for item in counts:                    
            lines.append("[{label}] ({count})".format(
                label = item.get("label", ""),
                count = int(item.get("count", 0))
            ))
        return "\n".join(lines) 


    @staticmethod
    def _spans_to_df(spans: list = []) -> DataFrame:    
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
    def _spans_to_csv(spans: list = [], sep=",") -> str:
        df = DocSummary._spans_to_df(spans)
        return df.to_csv(sep=sep)


    @staticmethod
    def _spans_to_html(spans: list = []) -> str:
        df = DocSummary._spans_to_df(spans)
        return(df.to_html(index=False, border=True)) # renders html table


    @staticmethod
    def _spans_to_html_list(spans: list = []) -> str:
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
    def _spans_to_json(spans: list = []) -> str:
        df = DocSummary._spans_to_df(spans)
        return df.to_json(orient="records")


    @staticmethod
    def _spans_to_list(spans: list = []) -> list:
        df = DocSummary._spans_to_df(spans)
        return df.to_dict(orient="records")


    @staticmethod
    def _spans_to_text(spans: list = []) -> str:
        df = DocSummary._spans_to_df(spans)
        pd.set_option('display.max_colwidth', None)
        return(df.to_string(index=False))
    

    @staticmethod
    def _tokens_to_df(toks: list = []) -> DataFrame:    
        return DataFrame([{
            "index": tok.i,
            "start": tok.idx + 1,
            "end": tok.idx + len(tok.text),
            "pos": tok.pos_,
            "text": tok.text,
            "lemma": tok.lemma_,
            } for tok in toks])  
    

    @staticmethod
    def _tokens_to_csv(toks: list = [], sep=",") -> str:
        df = DocSummary._tokens_to_df(toks)
        return df.to_csv(sep=sep)
            

    @staticmethod
    def _tokens_to_html(toks: list = []) -> str:
        df = DocSummary._tokens_to_df(toks)
        return df.to_html(index=False, border=0) # renders html table


    @staticmethod
    def _tokens_to_list(toks: list = []) -> list:
        df = DocSummary._tokens_to_df(toks)
        return df.to_dict(orient="records")        


    @staticmethod
    def _tokens_to_html_list(toks: list = []) -> str:
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
    def _tokens_to_json(toks: list = []) -> list:
        df = DocSummary._tokens_to_df(toks)
        return df.to_json(orient="records")


    @staticmethod
    def _tokens_to_text(toks: list = []) -> str:
        df = DocSummary._tokens_to_df(toks)
        pd.set_option('display.max_colwidth', None)
        return(df.to_string(index=False))


    @staticmethod
    def _tokens_to_text_custom(toks: list = []) -> str:
        lines = ["[{index}] ({start}->{end}) {pos:<4} \"{text}\"".format(
            index = tok.i,
            start = tok.idx + 1,
            end = tok.idx + len(tok.text),
            pos = tok.pos_,
            text = tok.text
            ) for tok in toks]
        return "\n".join(lines)


    # count spans by id, return list [{id, label, text, count}, {id, label, text, count}, ...] 
    # returned in descending count order - note there is probably a more elegant way to do this 
    @staticmethod   
    def _get_span_counts_by_id(
        spans: list = [], 
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
        spans_count = len(list(filter(lambda s: s.label_ not in exclude, spans)))

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


    # count spans by label, return list [{label, count}, {label, count}, ...] 
    # returned in descending count order
    @staticmethod   
    def _get_span_counts_by_label(
        spans: list = [], 
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

