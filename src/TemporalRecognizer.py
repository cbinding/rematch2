# =============================================================================
# Package   : rematch2
# Module    : TemporalRecognizer.py
# Version   : 20220427
# Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
# Contact   : ceri.binding@southwales.ac.uk
# Project   : ARIADNEplus
# Summary   : TemporalRecognizer class
# Imports   : json, spacy, os, fnmatch, argparse
# Example   : tr = TemporalRecognizer("en");
#             entities = tr.get_entities(input);
# License   : https://creativecommons.org/licenses/by/4.0/ [CC-BY]
# =============================================================================
# History
# 28/10/2021 CFB Initially created script
# 27/04/2022 CFB Added atomic entity types - ordinals, month names, season names
# =============================================================================
import argparse         # for argument parsing
import json
import fnmatch
import os               # for general file/directory functionality

import spacy            # NLP library
from spacy import displacy
#from spacy.pipeline import EntityRuler

#from LanguageEnum import LanguageEnum
from PeriodoData import PeriodoData
from TokenPatterns import TokenPatterns


class TemporalRecognizer:

    """identifies temporal entities in text based on array of predefined patterns"""
    def __init__(self, language="en", authority="", entity_types=[]):
        
        self._language = language

        # load language-specific pre-defined token patterns 
        #patterns = Recognizer.__load_token_patterns_from_directory("../src/patterns")
        #self._token_patterns = [pattern for pattern in patterns if (pattern.get("language") or "").lower() == self._language]
        tp = TokenPatterns()

        # prepare and configure language-specific spaCy pipeline 
        # TODO: if language property changes, this doesn't - maybe only allow language to be specified during init? 
        pipeline_name = ""
        if(self.language == "de"):
            pipeline_name = "de_core_news_sm"   # German
        elif(self.language == "es"):
            pipeline_name = "es_core_news_sm"   # Spanish
        elif(self.language == "fr"):
            pipeline_name = "fr_core_news_sm"   # French
        elif(self.language == "it"):
            pipeline_name = "it_core_news_sm"   # Italian
        elif(self.language == "nl"):
            pipeline_name = "nl_core_news_sm"   # Dutch
        elif(self.language == "no"):
            pipeline_name = "nb_core_news_sm"   # Norwegian Bokmal
        elif(self.language == "sv"):
            pipeline_name = "sv_core_news_sm"   # Swedish 
        else:
            pipeline_name = "en_core_web_sm"    # English (default)

        self._nlp = spacy.load(pipeline_name, disable = ['ner']) 
        self._nlp.max_length = 2000000  # TODO: don't recall why..         

        # configuration for spaCy entityRuler
        ruler_config = {
            "phrase_matcher_attr": "LOWER",
            "validate": True,
            "overwrite_ents": True, # overwrites overlapping entities
            "ent_id_sep": "||"
        }

        # add 'atomic' entityRuler patterns (date prefixes, suffixes etc.)
        ruler = self._nlp.add_pipe("entity_ruler", name="atomics", before="ner", config=ruler_config)
        atomic_entities = ["DATEPREFIX", "DATESUFFIX", "DATESEPARATOR", "ORDINAL", "MONTHNAME", "SEASONNAME"]
        #atomic_patterns = [pattern for pattern in self._token_patterns if (pattern.get("label") or "").upper() in atomic_entities]
        atomic_patterns = tp.get(self._language, atomic_entities)

        with self._nlp.select_pipes(enable="tagger"):
            ruler.add_patterns(atomic_patterns)

        # add 'composite' entityRuler patterns (year spans, century spans etc.)
        # composite patterns can refer to atomic patterns as entity types
        ruler = self._nlp.add_pipe("entity_ruler", name="composites", config=ruler_config)        
        composite_entities = ["TEMPORAL", "CENTURYSPAN", "YEARSPAN", "NAMEDPERIOD", "MONUMENT", "ARCHSCIENCE", "MATERIAL", "EVENTTYPE"] # TODO: revert to having these different categories
        #composite_patterns = [pattern for pattern in self._token_patterns if (pattern.get("label") or "").upper() in composite_entities]
        composite_patterns = tp.get(self.language, composite_entities)
        ruler.add_patterns(composite_patterns)

        # add terms from selected Perio.do authority as patterns
        pd = PeriodoData() # new instance, don't refresh cached data
        periods = pd.get_period_list(authority) # periods for authority id
        periodo_patterns = PeriodoData._periods_to_patterns(periods) # convert to spaCy pattern format
        ruler.add_patterns(periodo_patterns)
         

    @property
    def language(self):
        """language property used for entity recognition"""
        return self._language


    @language.setter
    def language(self, new_value):
        clean_value = new_value.strip().lower()
        if self._language != clean_value:
            self._language = clean_value

    
    def get_entities(self, text, format):
        """locate named entities in text based on token patterns"""        

        # normalise white spaces before tokenisation 
        # (extra spaces frustrate pattern matching)
        clean_input = " ".join(text.split())
        
        # find entities matching the token patterns         
        doc = self._nlp(clean_input)
                
        # temp - write current tokens to file, to aid debugging
        txt = ""
        for token in doc:
            txt += f"{token.text}\t{token.pos_}\t{token.head.text}\n"
        with open("tokens.txt", 'w', encoding='utf-8-sig') as f:
            f.write(txt)

        #with doc.retokenize() as retokenizer:
            #for ent in doc.ents:
               #retokenizer.merge(doc[ent.start:ent.end])

        # create and return array of entities
        results = []
        for entity in [e for e in doc.ents if e.label_ in ["TEMPORAL", "MONUMENT", "ARCHSCIENCE", "MATERIAL", "EVENTTYPE"]]:
            results.append({
                "id": entity.ent_id_,
                "text": entity.text,
                "start_char": entity.start_char,
                "end_char": entity.end_char,
                "type": entity.label_
            }) 
        # temp - describe current pipeline
        #print(self._nlp.pipe_names)
        #return results
        formatted = TemporalRecognizer.format_entities(clean_input, results, format)     
        return formatted


    @staticmethod
    def format_entities(text, ents, accept_format="application/json"):
        """convert entities to specified output format"""
        formatted = ""

        if accept_format.endswith("html"):
            formatted = TemporalRecognizer.__renderHTML(text, ents)
        elif accept_format.endswith("tab-separated-values") or accept_format.endswith("tsv"):
            formatted = TemporalRecognizer.__renderTSV(ents)
        elif accept_format.endswith("csv"):
            formatted = TemporalRecognizer.__renderCSV(ents)
        else: # default application/json
            formatted = TemporalRecognizer.__renderJSON(ents)
        
        return formatted


    @staticmethod
    def __renderHTML(text, ents):    
        # displacy requires this format as input     
        def formatter(ent):
            return { 
                "start": ent["start_char"], 
                "end": ent["end_char"], 
                "label": ent["type"] 
            }   
        
        data = {
            "text": text,
            "ents": list(map(formatter, ents))
        }  

        # return HTML rendering of input text with entities highlighted  
        options = {
            "ents": ["TEMPORAL", "MONUMENT", "EVENTTYPE", "MATERIAL", "ARCHSCIENCE"], #ents": ["TEMPORAL", "MONUMENT"],
            "colors": {
                "TEMPORAL": "lightgreen", 
                "MONUMENT": "lightblue",
                "EVENTTYPE": "lightgray",
                "MATERIAL": "steelblue",
                "ARCHSCIENCE": "orange"
            }
        }
        html = displacy.render(data, style="ent", manual=True, page=False, minify=True, options=options)
        return html


    @staticmethod
    def __renderJSON(ents):
        return json.dumps(ents)


    @staticmethod
    def __renderTSV(ents):         	
        return TemporalRecognizer.__renderDelimited(ents)


    @staticmethod
    def __renderCSV(ents):
        return TemporalRecognizer.__renderDelimited(ents, ",")


    @staticmethod
    def __renderDelimited(ents, delimiter="\t"):
        def escape_delimited(text):
            # todo - escape commas/tabs
            return str(text).replace("\\", "\\\\").replace("\"", "\\\"").replace(",", "\\,")

        lines = []
        for entity in ents:
            # create tab delimited line       
            line = "{id}{delim}{txt}{delim}{start}{delim}{end}{delim}{type}".format(
                delim=delimiter,
                id=escape_delimited(entity["id"]), 
                txt=escape_delimited(entity["text"]),
                start=escape_delimited(entity["start_char"]),
                end=escape_delimited(entity["end_char"]),
                type=escape_delimited(entity["type"])
                #lang = escapeDelimited(entity["lang"])
            )
            # add line to results
            lines.append(line)

        # return newline delimited lines	
        return "\n".join(lines)


# This class may be tested as a standalone script using the parameters below
#  e.g. python TemporalEntityRecognizer.py -i="the artefact was medieval or 1250-1275 or maybe post medieval"
if __name__ == "__main__":
    # initiate the input arguments parser
    parser = argparse.ArgumentParser(prog=__file__, 
        description='Identify named entities in free text')

    # add long and short argument descriptions
    parser.add_argument("-i", "--input",
        required=False, 
        default="",
        help="Input text extract to process")
    parser.add_argument("-l", "--language",
        required=False,
        default="en",
        choices=["de", "en", "es", "fr", "it", "nl", "no", "sv"],
        type=str.lower,
        help="ISO language (short code). If not provided the default assumed is 'en' (English)") 
    parser.add_argument("-p", "--periodo",
        required=False,
        default=None,
        type=str,
        help="Perio.do ID. If not provided Perio.do named periods will not be used")       
    parser.add_argument("-f", "--format",
        required=False,
        default="json",
        choices=["json","csv","tsv","html"],
        type=str.lower,
        help="Required output format. If not provided the default assumed is 'json'")
    parser.add_argument("-d", "--debug",
        required=False,
        default=False,
        help="Produces additional debugging info if true, for internal testing purposes")
    
    # parse and return args from command line
    args = parser.parse_args()

    # get cleaned named arguments
    input_text = ""
    language = "en"
    out_format = "json"
    is_debug = False
    periodo_id = "p0kh9ds" # temp default - HeritageData

    if args.input:
        input_text = args.input.strip()
    if args.format:
        out_format = args.format.strip().lower()
    if args.periodo:
        periodo_id = args.periodo.strip()
    if args.language:
        language = args.language.strip().lower()
    if args.debug:
        is_debug = True

    # identify named entities in text and output them
    # periodo_id examples: 
    # "p0kh9ds" - HeritageData (en)
    # "p02chr4" - PACTOLS chronology used in DOLIA data (fr)
    # "p0qhb66" - ARIADNE original collection (includes it)
    # "p0vn2fr" - Sök i samlingarna (sv)
    # "p04h98q" - Norsk arkeologisk leksikon (no)

    # example commands:
    # python3 TemporalRecognizer.py -l="de" -p="p0qhb66" -f="tsv" -i="Der Topf war mittelalterliche oder mittlere Bronzezeit oder 1257 bis 1575"
    # python3 TemporalRecognizer.py -l="en" -p="p0kh9ds" -f="tsv" -i="The pot was medieval or mid bronze age or 1257 to 1575" 
    # python3 TemporalRecognizer.py -l="es" -p="p0qhb66" -f="tsv" -i="La olla era medieval o de mediados de la edad de bronce o de 1257 a 1575." 
    # python3 TemporalRecognizer.py -l="fr" -p="p02chr4" -f="tsv" -i="Le pot est jurassique ou trias ou 1257 - 1575" 
    # python3 TemporalRecognizer.py -l="it" -p="p0qhb66" -f="tsv" -i="Il vaso era medievale o medio dell'età del bronzo o dal 1257 al 1575" 
    # python3 TemporalRecognizer.py -l="nl" -p="p0pqptc" -f="tsv" -i="De pot was middeleeuws of midden bronstijd of 1257 tot 1575" 
    # python3 TemporalRecognizer.py -l="no" -p="p04h98q" -f="tsv" -i="Potten var middelaldersk eller middels bronsealder eller 1257 til 1575" 
    # python3 TemporalRecognizer.py -l="sv" -p="p0vn2fr" -f="tsv" -i="Krukan var medeltid eller mellan bronsålder eller 1257 till 1575" 
    
    tr = TemporalRecognizer(language, periodo_id)
    entities = tr.get_entities(input_text, out_format)
    #formatted = TemporalRecognizer.format_entities(input_text, entities, out_format)
    print(entities)
