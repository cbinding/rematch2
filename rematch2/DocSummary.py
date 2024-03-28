"""
=============================================================================
Package   : rematch2
Module    : DocSummary.py
Classes   : DocSummary
Project   : Any
Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact   : ceri.binding@southwales.ac.uk
Summary   : Wrapper to summarise spaCy Doc spans, tokens & span pairs in
            various output formats. use to improve consistency in output
            TODO: to replace code in find_pairs.py & EntityPairs.py
Imports   : escape, DataFrame, Doc
Example   : as_html = DocSummary(doc).spans("html")
License   : https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History
14/03/2024 CFB Class combines code from other scripts to tidy things up
=============================================================================
"""
#from typing import Union
from html import escape
import pandas as pd
from pandas import DataFrame
from spacy.tokens import Doc
from spacy import displacy

if __package__ is None or __package__ == '':
    # uses current directory visibility
    from SpanPairs import SpanPairs
else:
    # uses current package visibility
    from .SpanPairs import SpanPairs

class DocSummary:

    def __init__(self, doc: Doc):
        self._doc = doc
    

    def __str__(self):
        pass


    def __repr__(self):
        return self.__str__()


    def doctext(self, format: str="text") -> str: 
        match format.strip().lower():  
            case "html": return self._doctext_to_html(self._doc)
            case _: return self._doc.text

    #sentences?

    def spans(self, format: str="text") -> str|list:
        spans = self._doc.spans["custom"]
        match format.strip().lower():
            case "csv": return self._spans_to_csv(spans)
            case "html": return self._spans_to_html(spans)
            case "htmll": return self._spans_to_html_list(spans)
            case "json": return self._spans_to_json(spans)
            case "text": return self._spans_to_text(spans)
            case _: return spans


    def spanpairs(self, format: str="text", left_types: list=[], right_types: list=[], rel_ops: list=[]) -> str|list:
        pairs = SpanPairs(doc=self._doc, rel_ops=rel_ops, left_types=left_types, right_types=right_types).pairs
        match format.strip().lower():
            case "csv": return self._spanpairs_to_csv(pairs)
            case "html": return self._spanpairs_to_html(pairs)   # render as a table
            case "htmll": return self._spanpairs_to_html_list(pairs) # render as a list
            case "htmlc": return self._spanpairs_to_html_custom(pairs) # rendering from find_pairs.py
            case "json": return self._spanpairs_to_json(pairs)
            case "text": return self._spanpairs_to_text(pairs)
            case _: return pairs

    
    def spancounts(self, format: str="text") -> str|list:
        counts = self._get_span_counts_by_id(self._doc.spans["custom"])
        match format.strip().lower():
            case "csv": return self._spancounts_to_csv(counts)
            case "html": return self._spancounts_to_html(counts) # render as a table
            case "htmll": return self._spancounts_to_html_list(counts) # render as a list
            case "htmlc": return self._spancounts_to_html_custom(counts) # rendering from find_pairs.py
            case "json": return self._spancounts_to_json(counts)
            case "text": return self._spancounts_to_text(counts)
            case _: return counts


    def tokens(self, format: str="text") -> str|list:
        toks = self._doc
        match format.strip().lower():
            case "csv": return self._tokens_to_csv(toks)
            case "html": return self._tokens_to_html(toks)  # render as a table
            case "htmll": return self._tokens_to_html_list(toks) # render as a list
            case "json": return self._tokens_to_json(toks)            
            case "text": return self._tokens_to_text(toks)
            case _: return toks

    
    @staticmethod
    def _doctext_to_html(doc: Doc, options=None) -> str:
        opts = { 
            "spans_key": "subset",
            "colors": { 
                #"DATEPREFIX": "lightgray",
                #"DATESUFFIX": "lightgray",
                #"ORDINAL": "lightgray",
                "NEGATION": "lightgray",
                "PERIOD": "yellow", 
                "YEARSPAN": "moccasin", 
                "OBJECT": "plum",
                "MONUMENT": "plum",
                "ARCHSCIENCE": "lightpink",
                "EVIDENCE": "aliceblue",
                "MATERIAL": "antiquewhite",
                "EVENTTYPE": "coral"
            } 
        } if options == None else options 

        # create temporary subset as options don't allow us to specify which spans to show/exclude
        def to_display(span): return span.label_ not in ["DATEPREFIX", "DATESUFFIX", "DATESEPARATOR", "ORDINAL"]
        doc.spans["subset"] = list(filter(to_display, doc.spans["custom"]))         
        #return displacy.render(doc, style="ent", minify=True, options=opts) 
        html = displacy.render(doc, style="span", page=False, minify=False, jupyter=False, options=opts) 
        del doc.spans["subset"]
        return html
   

    @staticmethod
    def _spanpairs_to_df(pairs: list = []) -> DataFrame:
        return DataFrame([{
            "span1_id": pair.span1.id_,
            "span1_type": pair.span1.label_,
            "span1_text": pair.span1.text,
            "rel_op": pair.rel_op,
            "span2_id": pair.span2.id_,
            "span2_type": pair.span2.label_,
            "span2_text": pair.span2.text,
            "score": pair.score
        } for pair in pairs])
        

    @staticmethod
    def _spanpairs_to_csv(pairs: list = [], sep=",") -> str:
        df = DocSummary._spanpairs_to_df(pairs)
        return df.to_csv(sep=sep)


    @staticmethod
    def _spanpairs_to_html(pairs: list = []) -> str:
        df = DocSummary._spanpairs_to_df(pairs)
        return(df.to_html(index=False, border=0)) # renders html table


    @staticmethod
    def _spanpairs_to_htmll(pairs: list = []) -> str:
        pass

    # custom table render from find_pairs.py 
    @staticmethod
    def _spanpairs_to_html_custom(pairs: list = []) -> str:
        html = []
        if len(pairs) == 0:
            html.append("<p>NONE FOUND</p>")
        else:
            html.append("<table><tbody>")
            for pair in pairs:
                html.append("<tr>")
                html.append("<td style='text-align:right; vertical-align: middle;'>")
                html.append(f"<div class='entity {escape(pair.span1.label_.lower())}'>")
                if(pair.span1.id_.startswith("http")):
                    html.append(f"<a href='{pair.span1.id_}'>{escape(pair.span1.text)}</a>")
                else:
                    html.append(f"{escape(pair.span1.text)}")
                html.append("</div></td>")                    
                html.append(f"<td style='text-align:left; vertical-align: middle'>")
                html.append(f"<div class='entity {escape(pair.span2.label_.lower())}'>")
                if(pair.span2.id_.startswith("http")):
                    html.append(f"<a href='{pair.span2.id_}'>{escape(pair.span2.text)}</a>")
                else:
                    html.append(f"{escape(pair.span2.text)}")
                html.append("</div></td>")
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
            "id": item["id"],
            "type": item["type"],
            "text": item["text"],
            "count": item["count"]
            } for item in counts]) 


    @staticmethod
    def _spancounts_to_csv(counts: list = [], sep=",") -> str:
        df = DocSummary._spancounts_to_df(counts)
        return df.to_csv(sep=sep)


    @staticmethod
    def _spancounts_to_html(counts: list = []) -> str:
        df = DocSummary._spancounts_to_df(counts)
        return(df.to_html(index=False, border=0)) # renders html table

    # table rendering from find_pairs.py
    @staticmethod
    def _spancounts_to_html_custom(counts: list = []) -> str:
        html = []        
        if len(counts) == 0:
            html.append("<p>NONE FOUND</p>")
        else:
            html.append("<table><tbody>")
            for item in counts:
                html.append("<tr>")
                html.append("<td style='text-align:right; vertical-align: middle;'>")
                html.append(f"<div class='entity {escape(item['type'].lower())}'>")
                if(item['id'].startswith("http")):
                    html.append(f"<a href='{item['id']}'>{escape(item['text'])}</a>")
                else:
                    html.append(f"{escape(item['text'])}")
                html.append("</div>")
                html.append("</td>")
                html.append(f"<td>({item['count']})</td>")
                html.append("</tr>")
            html.append("</tbody></table>")
        return "\n".join(html)


    @staticmethod
    def _spancounts_to_htmll(counts: list = []) -> str:
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
            lines.append("[{type}] {id:<60} {text:>20} ({count})".format(
                id = item["id"],                
                type = item["type"],
                text = item["text"],
                count = item["count"]
                )
            )
        return "\n".join(lines) 
    

    @staticmethod
    def _spans_to_df(spans: list = []) -> DataFrame:    
        return DataFrame([{
            "start": span.start_char + 1,
            "end": span.end_char,
            "type": span.label_,
            "id": span.ent_id_,
            "text": span.text
            } for span in spans]) 


    @staticmethod
    def _spans_to_csv(ents: list = [], sep=",") -> str:
        df = DocSummary._spans_to_df(spans)
        return df.to_csv(sep=sep)


    @staticmethod
    def _spans_to_html(spans: list = []) -> str:
        df = DocSummary._spans_to_df(ents)
        return(df.to_html(index=False, border=0)) # renders html table


    @staticmethod
    def _spans_to_html_list(spans: list = []) -> str:
        html = []
        html.append("<details>")
        html.append(f"<summary>Entities ({len(spans)})</summary>")
        html.append("<ul class='entities'>") 
        for span in spans:
            html.append(f"<li class='entity {type.lower()}'>({start}&#8594;{end}) [{type}] {id} \"{text}\"</li>".format(
                start = span.start_char + 1,
                end = span.end_char,
                type = span.label_,
                id = span.ent_id_,
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
    def _tokens_to_html(toke: list = []) -> str:
        df = DocSummary._tokens_to_df(toks)
        return df.to_html(index=False, border=0) # renders html table


    @staticmethod
    def _tokens_to_html_list(toks: list = []) -> str:
        html = []
        html.append("<ul class='tokens'>")
        for tok in toks:
            html.append("<li class='token'>[{index}] ({start}&#8594;{end}) {pos:<4} \"{text}\"</li>".format(
                index = tok.i,
                start = tok.idx + 1,
                end = tok.idx + len(tok.text),
                pos = tok.pos_,
                text = escape(tok.text)                
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


    # count spans by id, return list [{id, type, text, count}, {id, type, text, count}, ...] 
    # returned in descending count order - note there is probably a more elegant way to do this 
    @staticmethod   
    def _get_span_counts_by_id(spans: list = []) -> list:
        counts = {}

        for span in spans:
            # don't include these in summary counts?
            if span.label_ in ["NEGATION", "DATEPREFIX", "DATESEPARATOR", "DATESUFFIX", "ORDINAL"]:
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
            
            # create a new record if not encountered before, or increment the count
            if id not in counts:
                counts[id] = { "id": id, "type": span.label_, "text": span.lemma_, "count": 1 } 
            else:
                counts[id]["count"] += 1            
        
        # return as list sorted by ascending count
        return sorted(list(counts.values()), key=lambda x: x.get("count", 0), reverse=True)


    # custom along the lines of displacy but locally controllable styling?
    # TODO: not finished or used anywhere yet...
    @staticmethod
    def _custom_html_rendering(doc: Doc) -> str:
        
        def render_in_tag(tag_name: str, content: str):
            return f"<{escape(tag_name)}>{escape(content)}></{escape(tag_name)}>"

        def tok_for_render(tok):
            return {
                "index": tok.idx,
                "text": tok.text_with_ws,
                "label": None
            }

        def span_for_render(span):
            return {
                "index": span.start,
                "text": span.text,
                "label": span.label_
            }

        toks_outside_spans = list(filter(lambda t: t.ent_iob_ not in ['B', 'I'], doc)) 
        toks_for_render = list(map(tok_for_render, toks_outside_spans))
        spans_for_render = list(map(span_for_render, doc.spans["custom"]))
        items_for_render = sorted(toks_for_render + spans_for_render, key=lambda x: x.get("index", 0))

        html = "<div>"
        for item in items_for_render:
            if item["label"] is not None:
                html += f"<mark class='entity {escape(item['label'].lower())}'>{escape(item['text'])}</mark>"
            else:
                html += item["text"] 
        html += "</div>"
        return html