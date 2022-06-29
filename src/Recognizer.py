# =============================================================================
# Package   : rematch
# Module    : Recognizer.py
# Version   : 20220427
# Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
# Contact   : ceri.binding@southwales.ac.uk
# Project   : ReMatch
# Summary   : Recognizer class
# Imports   : json, spacy, os, fnmatch, argparse
# Example   : ner = Recognizer("en");
#             ents = ner.get_entities(input);
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

from PeriodoData import PeriodoData

class Recognizer:
    """identifies and marks up temporal entities based on array of patterns"""
    def __init__(self, lang="en"):
        self._language = lang.strip().lower()
        self._all_token_patterns = Recognizer.__load_token_patterns_from_directory("../src/patterns")
        #self._nlp = self.__getNLP() # sets up configured nlp pipeline object  

    @property
    def language(self):
        """language property used for entity recognition"""
        return self._language

    @language.setter
    def language(self, new_value):
        clean_value = new_value.strip().lower()
        if self._language != clean_value:
            self._language = clean_value            
    
    @staticmethod
    def __load_token_patterns_from_directory(directory_name):
        """Load token patterns from JSON files situated in the specified directory"""
        file_names = os.listdir(directory_name)
        token_patterns = []

        for file_name in fnmatch.filter(file_names, "*.json"):
            file_name_with_path = os.path.join(directory_name, file_name)
            token_patterns.extend(Recognizer.__load_json_from_file(file_name_with_path))
        return token_patterns 

    @staticmethod
    def __load_json_from_file(file_name_with_path):
        """Load data from one specified (JSON) file"""
        json_data = []
        with open(file_name_with_path, 'r', encoding='utf8') as f:
            json_data = json.load(f)
        return json_data

    # get pre-configured spaCy trained NLP object
    #def __getNLP(self):
        # get language-specific pipeline
        #if(self._language == "fr"):
            #nlp = spacy.load("fr_core_news_sm")
        #elif(self._language == "no"):
            #nlp = spacy.load("nb_core_news_sm")
        #else:
        #nlp = spacy.load("en_core_web_sm", disable = ['ner'])
        #nlp = spacy.blank(self._language) # cant use POS with this

        #nlp.max_length = 2000000
        #nlp.vocab.strings.add('DATEPREFIX')
        # Add configured entity ruler to the pipeline
        #rulerConfig = {
        #    "phrase_matcher_attr": "LOWER",
        #    "validate": True,
        #    "overwrite_ents": True, # overwrites overlapping entities
        #    "ent_id_sep": "||"
        #}
        # https://stackoverflow.com/questions/57536896/custom-entity-ruler-with-spacy-did-not-return-a-match?noredirect=1&lq=1
        # 2 stages TO achieve nested NER (i.e. referring to custom ENT_TYPE in TOKEN PATTERN)

        #ruler = EntityRuler(nlp, phrase_matcher_attr="LOWER", overwrite_ents=True, ent_id_sep="||", validate=True)
        #with nlp.select_pipes(enable="tagger"):
            #ruler.add_patterns(patterns)
        #nlp.add_pipe(ruler, before="ner")
        #ruler = nlp.add_pipe("entity_ruler",name="atomics", before="ner", config=rulerConfig)
    
        # adding 'atomic' patterns to the entity ruler
        #patterns = list(filter(lambda pattern: pattern["label"] or None in ["DATEPREFIX", "DATESUFFIX"] and pattern["language"] or None == self._language, self._allTokenPatterns)) 
        #patterns = [patt for patt in self._allTokenPatterns if patt.get("label") in ["DATEPREFIX", "DATESUFFIX"] and patt.get("language") == self._language] 
        #ruler.add_patterns(patterns)

        # add (language-specific) token patterns to the entity ruler
        #patterns = filter(lambda pattern: pattern["label"] or None in [self._entityType] and pattern["language"] or None == self._language, self._allTokenPatterns)       
        #ruler.add_patterns(patterns)
        # this may be faster? see https://spacy.io/usage/rule-based-matching
        # with nlp.select_pipes(enable="tagger"):
           #ruler.add_patterns(patterns)
        #return nlp    
    
    def get_entities(self, text):
        """locate named entities in text based on token patterns"""
        # prepare language-specific spaCy NLP object        
        nlp = None        
        if(self._language == "fr"):
            nlp = spacy.load("fr_core_news_sm")
        elif(self._language == "no"):
            nlp = spacy.load("nb_core_news_sm")
        else:
            nlp = spacy.load("en_core_web_sm", disable = ['ner'])            

        # dont recall why.. TODO: find out.. 
        nlp.max_length = 2000000

        # configuration for spaCy entityRuler
        ruler_config = {
            "phrase_matcher_attr": "LOWER",
            "validate": True,
            "overwrite_ents": True, # overwrites overlapping entities
            "ent_id_sep": "||"
        }

        # pipeline component adding (language specific) 'atomic' entityRuler patterns (date prefixes, suffixes etc.)
        ruler = nlp.add_pipe("entity_ruler", name="atomics", before="ner", config=ruler_config)
        atomic_entities = ["DATEPREFIX", "DATESUFFIX", "ORDINAL", "MONTHNAME", "SEASONNAME"]
        atomic_patterns = [pattern for pattern in self._all_token_patterns if (pattern.get("label") or "").upper() in atomic_entities and (pattern.get("language") or "").lower() == self._language]
        with nlp.select_pipes(enable="tagger"):
            ruler.add_patterns(atomic_patterns)

        # pipeline component adding (language specific) 'composite' entityRuler patterns (year spans, century spans etc.)
        # The composite pattermns can refer to artomic patterns
        ruler = nlp.add_pipe("entity_ruler", name="composites", config=ruler_config)        
        #nlp.add_pipe("merge_entities")
        #patterns = filter(lambda pattern: pattern["label"] or None in [self.entityType] and pattern["language"] or None == self._language, self._allTokenPatterns) 
        composite_patterns = [pattern for pattern in self._all_token_patterns if (pattern.get("label") or "").lower() == "temporal" and (pattern.get("language") or "").lower() == self._language] 
        ruler.add_patterns(composite_patterns)

        # add selected Perio.do terms as patterns
        authority_id = "p0kh9ds" # temp hardcoded (HeritageData)
        pd = PeriodoData(False) # creating new instance, don't refresh cache
        periods = pd.get_period_list(authority_id)
        periodo_patterns = PeriodoData._periods_to_patterns(periods)
        ruler.add_patterns(periodo_patterns)

        # normalise white spaces before tokenisation 
        # (extra spaces frustrate pattern matching)
        clean_input = " ".join(text.split())
        
        # find entities matching the token patterns         
        doc = nlp(clean_input)
                
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
        for entity in [e for e in doc.ents if e.label_ == "TEMPORAL"]:
            results.append({
                "id": entity.ent_id_,
                "text": entity.text,
                "start_char": entity.start_char,
                "end_char": entity.end_char,
                "type": entity.label_
            })       
        return results

    @staticmethod
    def format_entities(text, ents, accept_format="application/json"):
        """convert entities to specified output format"""
        formatted = ""

        if accept_format.endswith("html"):
            formatted = Recognizer.__renderHTML(text, ents)
        elif accept_format.endswith("tab-separated-values") or accept_format.endswith("tsv"):
            formatted = Recognizer.__renderTSV(ents)
        elif accept_format.endswith("csv"):
            formatted = Recognizer.__renderCSV(ents)
        else: # default application/json
            formatted = Recognizer.__renderJSON(ents)
        
        return formatted

    @staticmethod
    def __renderHTML(text, ents):    
        # displacy requires this format as input     
        def formatter(e):
            return { "start": e["start_char"], "end": e["end_char"], "label": e["type"] }   
        data = {
            "text": text,
            "ents": list(map(formatter, ents))
        }  
        # get html rendering of input text with entities highlighted  
        options = {
            "ents": ["TEMPORAL"],
            "colors": {"TEMPORAL": "lightgreen"}
        }
        html = displacy.render(data, style="ent", manual=True, page=False, minify=True, options=options)
        return html

    @staticmethod
    def __renderJSON(ents):
        return json.dumps(ents)

    @staticmethod
    def __renderTSV(ents):         	
        return Recognizer.__renderDelimited(ents)

    @staticmethod
    def __renderCSV(ents):
        return Recognizer.__renderDelimited(ents, ",")

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
        help="Input text extract to process")
    parser.add_argument("-l", "--language",
        required=False,
        default="en",
        choices=["en","fr","sv"],
        type=str.lower,
        help="ISO language (short code). If not provided the default assumed is 'en' (English)") 
    parser.add_argument("-p", "--periodo",
        required=False,
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
    language = ""
    out_format = "json"
    is_debug = False
    periodo = None

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
    # TODO: use periodo_id here..
    ner = Recognizer(language)
    entities = ner.get_entities(input_text)
    formatted = Recognizer.format_entities(input_text, entities, out_format)
    print(formatted)
