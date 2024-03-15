"""
=============================================================================
Package :   rematch2
Module  :   BaseRuler.py
Classes :   BaseRuler
Version :   20231027
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy custom pipeline component (specialized EntityRuler)
Imports :   EntityRuler, Language
Example :   N/A - superclass for more specialized components    
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History :   
10/10/2023 CFB Added language factory function
27/10/2023 CFB type hints added for function signatures
=============================================================================
"""
import json
import os
import sys
from pathlib import Path
from collections.abc import MutableSequence
from enum import Enum
import spacy
from spacy.pipeline import EntityRuler
from spacy.tokens import Doc
from spacy.language import Language
from pprint import pprint

import pandas as pd

if __package__ is None or __package__ == '':
    # uses current directory visibility
    from VocabularyEnum import VocabularyEnum
    from spacypatterns import *
else:
    # uses current package visibility
    from .VocabularyEnum import VocabularyEnum
    from .spacypatterns import *


class BaseRuler(EntityRuler):

    def __init__(
        self,
        nlp: Language,
        name: str = "base_ruler",
        lemmatize: bool = True,
        pos: MutableSequence = [],
        min_term_length: int = 3,
        min_lemmatize_length: int = 4,
        default_label: str = "UNKNOWN",
        patterns: MutableSequence = []
    ) -> None:

        EntityRuler.__init__(
            self,
            nlp=nlp,
            name=name,
            phrase_matcher_attr="LOWER",
            validate=False,
            overwrite_ents=True,
            ent_id_sep="||"
        )
        '''
        # is this the same as saying:
        super().__init__(
            self,
            nlp=nlp,
            name=name,
            phrase_matcher_attr="LOWER",
            validate=False,
            overwrite_ents=True,
            ent_id_sep="||"
        )'''

        # patterns: [{id, label, language, pattern}, {id, label, language, pattern},...]
        patterns_to_add = []
        for item in patterns:
            # clean input values before using
            clean_id = BaseRuler.normalize_whitespace(item.get("id", ""))
            clean_label = BaseRuler.normalize_whitespace(item.get("label", default_label))
            pattern = item.get("pattern", "")

            # is there even a pattern present? 
            # (at this point it may be a list or a str)
            if len(pattern) > 0:

                # if token pattern  [{},{}]
                if isinstance(pattern, list):

                    # add to list of patterns_to_add
                    patterns_to_add.append({
                        "id": clean_id,
                        "label": clean_label,
                        "pattern":  pattern
                    })

                # if phrase pattern (plain string term/phrase)   
                elif isinstance(pattern, str):
                    
                    # normalize whitespace (inconsistent whitespace can frustrate matching)
                    clean_phrase = BaseRuler.normalize_whitespace(pattern)
                    
                    # if too small don't include it at all
                    if len(clean_phrase) < min_term_length:
                        continue

                    # first tokenize the phrase
                    doc = nlp(clean_phrase)
                    phrase_length = len(doc)
                    
                    # build a new pattern for this phrase
                    new_pattern = []                    
                    # for each term (token) in the phrase
                    for n, tok in enumerate(doc, 1):
                        pat = {}

                        # lemmatize term if required (and if term is long enough)
                        # e.g. "skirting boards":
                        # { "LEMMA": "skirt" }, { "LEMMA": "board" } or
                        # { "LOWER": "skirt" }, { "LOWER": "board" }
                        # IMPORTANT: lemmatization doesn't work where text is
                        # capitalised, as spaCy mistakes it for a proper Noun
                        if (lemmatize and len(tok.text) >= min_lemmatize_length):
                            pat["LEMMA"] = tok.lemma_.lower()
                        else:
                            pat["LOWER"] = tok.text.lower()  
                    
                        # add pos tags if passed in
                        # note POS only applied to LAST term if multi-word phrase
                        # e.g. { "LEMMA": "board", "POS": { "IN": ["NOUN", "PROPN"] }}
                        if (len(pos) > 0 and n == phrase_length):
                            pat["POS"] = {"IN": pos}

                        new_pattern.append(pat)

                    # add newly built pattern to list of patterns
                    # print(new_pattern)
                    patterns_to_add.append({
                        "id": clean_id,
                        "label": clean_label,
                        "pattern":  new_pattern
                    })
            
        # finally, add all new patterns to the underlying EntityRuler
        if len(patterns_to_add) > 0:
            self.add_patterns(patterns_to_add) 
            #print(patterns_to_add)



    # new - experimental (static) functions to make things less complicated?
    @staticmethod
    def normalize_whitespace(s: str = ""): 
        return ' '.join(s.strip().split())   
    

    @staticmethod
    # not used yet
    def convert_string_to_pattern(s: str = "", preserve_case: bool = False)-> list: 
        clean_s = BaseRuler.normalize_whitespace(s) #.replace("\"", "\\\"")
        item = {}
        if(preserve_case):
           item["TEXT"] = clean_s 
        else:
            item["LOWER"] = clean_s.lower()
        return [item]


    @staticmethod
    # not used yet - add pos list to last element in a pattern
    def add_pos_to_last_pattern_element(pattern: list=[], pos: list=[]) -> list:                           
        if len(pattern) > 0 and len(pos) > 0:
            pattern[-1]["POS"] = { "IN": pos }
        return pattern
        

    def __call__(self, doc: Doc) -> Doc:
        EntityRuler.__call__(self, doc)
        #pprint(doc)        
        return doc


    @staticmethod
    def _get_patterns_from_json_file(file_name: str) -> MutableSequence:
        base_path = (Path(__file__).parent / "vocabularies").resolve()
        file_path = os.path.join(base_path, file_name)
        patterns = []
        with open(file_path, "r") as f:
            patterns = json.load(f)

        return patterns


    @staticmethod
    def _get_patterns_from_enum(vocab: VocabularyEnum) -> MutableSequence:
        return BaseRuler._get_patterns_from_json_file(vocab.value)


@Language.factory(name="amcr_ruler")
def create_amcr_ruler(nlp: Language, name: str = "amcr_ruler") -> BaseRuler:
    return BaseRuler(
        nlp=nlp,
        name=name,
        default_label="AMCR",
        patterns=_get_patterns_from_json_file()
    )

@Language.factory(name="aat_activities_ruler")
def create_aat_activities_ruler(nlp: Language, name: str = "aat_activities_ruler") -> BaseRuler:
    return BaseRuler(
        nlp=nlp,
        name=name,
        default_label="ACTIVITY",
        patterns=patterns_en_AAT_ACTIVITIES
    )


@Language.factory("aat_agents_ruler")
def create_aat_agents_ruler(nlp: Language, name: str="aat_agents_ruler") -> BaseRuler:
    return BaseRuler(
        nlp=nlp,
        name=name,
        pos=["NOUN", "PROPN"],
        default_label="AGENT",
        patterns=patterns_en_AAT_AGENTS
    )


@Language.factory("aat_associated_concepts_ruler")
def create_aat_associated_concepts_ruler(nlp: Language, name: str="aat_associated_concepts_ruler") -> BaseRuler:
    return BaseRuler(
        nlp=nlp,
        name=name,
        default_label="ASSOCIATED_CONCEPT",
        patterns=patterns_en_AAT_ASSOCIATED_CONCEPTS
    )


@Language.factory("aat_materials_ruler")
def create_aat_materials_ruler(nlp: Language, name: str="aat_materials_ruler") -> BaseRuler:
    return BaseRuler(
        nlp=nlp,
        name=name,
        default_label="MATERIAL",
        patterns=patterns_en_AAT_MATERIALS
    )


@Language.factory("aat_objects_ruler")
def create_aat_objects_ruler(nlp: Language, name: str="aat_objects_ruler") -> BaseRuler:
    return BaseRuler(
        nlp=nlp,
        name=name,
        pos=["NOUN", "PROPN"],
        default_label="OBJECT",
        patterns=patterns_en_AAT_OBJECTS
    )


@Language.factory("aat_physical_attributes_ruler")
def create_aat_physical_attributes_ruler(nlp: Language, name: str="aat_physical_attributes_ruler") -> BaseRuler:
    return BaseRuler(
        nlp=nlp,
        name=name,
        default_label="PHYSICAL_ATTRIBUTE",
        patterns=patterns_en_AAT_PHYSICAL_ATTRIBUTES
    )


@Language.factory("aat_styleperiods_ruler")
def create_aat_styleperiods_ruler(nlp: Language, name: str="aat_styleperiods_ruler") -> BaseRuler:
    return BaseRuler(
        nlp=nlp,
        name=name,
        default_label="STYLEPERIOD",
        patterns=patterns_en_AAT_STYLEPERIODS
    )


@Language.factory("fish_archobjects_ruler")
def create_fish_archobjects_ruler(nlp: Language, name: str="fish_archobjects_ruler") -> BaseRuler:
    return BaseRuler(
        nlp=nlp,
        name=name,
        pos=["NOUN", "PROPN"],
        default_label="OBJECT",
        patterns=patterns_en_FISH_ARCHOBJECTS
    )


@Language.factory("fish_archsciences_ruler")
def create_fish_archsciences_ruler(nlp: Language, name: str="fish_archsciences_ruler") -> BaseRuler:
    return BaseRuler(
        nlp=nlp,
        name=name,
        default_label="ARCHSCIENCE",
        patterns=patterns_en_FISH_ARCHSCIENCES
    )


@Language.factory("fish_building_materials_ruler")
def create_fish_building_materials_ruler(nlp: Language, name: str="fish_building_materials_ruler") -> BaseRuler:
    return BaseRuler(
        nlp=nlp,
        name=name,
        default_label="MATERIAL",
        patterns=patterns_en_FISH_BUILDING_MATERIALS
    )


@Language.factory("fish_components_ruler")
def create_fish_components_ruler(nlp: Language, name: str="fish_components_ruler") -> BaseRuler:
    return BaseRuler(
        nlp=nlp,
        name=name,
        pos=["NOUN", "PROPN"],
        default_label="OBJECT",
        patterns=patterns_en_FISH_COMPONENTS
    )


@Language.factory("fish_event_types_ruler")
def create_fish_event_types_ruler(nlp: Language, name: str="fish_event_types_ruler") -> BaseRuler:
    return BaseRuler(
        nlp=nlp,
        name=name,
        default_label="EVENT",
        patterns=patterns_en_FISH_EVENT_TYPES
    )


@Language.factory("fish_evidence_ruler")
def create_fish_evidence_ruler(nlp: Language, name: str="fish_evidence_ruler") -> BaseRuler:
    return BaseRuler(
        nlp=nlp,
        name=name,
        default_label="EVIDENCE",
        patterns=patterns_en_FISH_EVIDENCE
    )


@Language.factory("fish_maritime_craft_ruler")
def create_fish_maritime_craft_ruler(nlp: Language, name: str="fish_maritime_craft_ruler") -> BaseRuler:
    return BaseRuler(
        nlp=nlp,
        name=name,
        pos=["NOUN", "PROPN"],
        default_label="OBJECT",
        patterns=patterns_en_FISH_MARITIME_CRAFT
    )


@Language.factory("fish_monument_types_ruler")
def create_fish_monument_types_ruler(nlp: Language, name: str="fish_monument_types_ruler") -> BaseRuler:
    return BaseRuler(
        nlp=nlp,
        name=name,
        pos=["NOUN", "PROPN"],
        default_label="OBJECT",
        #min_lemmatize_length=3,
        patterns=patterns_en_FISH_MONUMENT_TYPES
    )


@Language.factory("fish_periods_ruler")
def create_fish_periods_ruler(nlp: Language, name: str="fish_periods_ruler") -> BaseRuler:
    return BaseRuler(
        nlp=nlp,
        name=name,
        default_label="PERIOD",
        patterns=patterns_en_FISH_PERIODS
    )


# test the BaseRuler class
if __name__ == "__main__":

    # sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    # from rematch2.spacypatterns import vocab_en_AAT_OBJECTS
    # from ..spacypatterns import vocab_en_AAT_OBJECTS

    test_text1 = '''Aside from three residual flints, none closely datable, the earliest remains comprised a small assemblage of Roman pottery and ceramic building material, also residual and most likely derived from a Roman farmstead found immediately to the north within the Phase II excavation area. A single sherd of Anglo-Saxon grass-tempered pottery was also residual. The earliest features, which accounted for the majority of the remains on site, relate to medieval agricultural activity focused within a large enclosure. There was little to suggest domestic occupation within the site: the pottery assemblage was modest and well abraded, whilst charred plant remains were sparse, and, as with some metallurgical residues, point to waste disposal rather than the locations of processing or consumption. A focus of occupation within the Rodley Manor site, on higher ground 160m to the north-west, seems likely, with the currently site having lain beyond this and providing agricultural facilities, most likely corrals and pens for livestock. Animal bone was absent, but the damp, low-lying ground would have been best suited to cattle. An assemblage of medieval coins recovered from the subsoil during a metal detector survey may represent a dispersed hoard.'''
    test_text2 = '''
    mola conducted an archaeological desk-based heritage assessment of land at fakenham road, great ryburgh, norfolk. the earliest archaeological evidence found dates from the mesolithic period. neolithic flint tools have been found close to the west and north-west of the site. a possible bronze age ring ditch has been identified to the north-east and finds dating to the period have been discovered through metal detecting surveys. iron age remains including pits and pottery have been found within the area of proposed development through trial trenching. the site lies between two roman settlements on the south-western banks of the river wensum. one lies nearby to the north-west of the site and numerous finds including coins have been discovered during a fieldwalking survey. a further roman settlement lies to the south-east where two enclosures, two kilns and two burials have recently been excavated. a middle saxon cemetery, drainage ditches, an enclosure, land divisions and a substantial boundary ditch have also recently been discovered to the south-east of the site. metal finds dating to the period have also been found to the north-west and to the east of the site during metal detecting surveys. the site lies beyond the historic core of great ryburgh. the medieval settlement developed around the junction of fakenham road and bridge road to the west of the river wensum, flanked by the medieval moated manor of ryburgh at the northern end and by st andrew's church to the south. cartographic evidence suggests that the site lay to the rear of properties fronting fakenham road during the post-medieval period and had remained as undeveloped farmland.'''
    test_text3 = '''
    The Excavation revealed a wealth of archaeological information. The earliest period was represented by residual finds of a Mesolithic worked flint axe in a medieval plough furrow and Bronze Age aurochs bone in an Iron Age pit. The Iron Age period consisted of several phases of a Banjo Enclosure with associated roundhouses, four-post structures, boundary ditches, pits and a quarry. In the early Roman period there was little activity other than quarrying, but later a farmstead was established with an agricultural system reminiscent of a vineyard. No evidence was recovered for the Saxon period, even as residual finds in later contexts, and thus it is assumed that the site was either unused by the population at that time, or subject to a regime that has left no trace in the archaeological record. In the medieval period a ridge and furrow cultivation system was established that cut across many earlier features but incorporated surprisingly little material from earlier periods. After the medieval period, the site appears to have been largely abandoned until Enclosure. The two phases of work took place between March - May 2000 and subsequently between August - October 2001 by CAM ARC, Cambridgeshire County Council (formerly the Archaeological Field Unit).
    '''
    test_text4 = '''
    in autumn 2008 a programme of archaeological excavation was undertaken  at titnore lane, goring-by-sea.  the excavation was conducted across the full area of the 2.2 hectare site.    a wide range of periods were represented on site, incorporating the mesolithic, neolithic, bronze age, iron age, romano-british, medieval, and later post-medeival activity. the features and finds assemblage associated with the mesolithic and neolithic were limited, representing only a periodic use of the site. the key feature associated with mid to late bronze age activity was a c.3.5m wide trackway identified as running north-south across the site. by the late bronze age/early iron age period the first evidence of settlement was identified, formed of a roundhouse, pits and a possible livestock corral. the mid to late iron age period saw a growth in settlement with several phases of roundhouse construction associated with boundary ditches, pitting, further possible corrals and  the creation of an artificial pond adjacent to the settlement. the settlement had disappeared by the 1st century ad replaced by a series of field boundaries and rubbish pits thought to part of the villa complex known immediately to the south of the site. romano-british activity did not survive beyond the early to mid 2nd century. a large enclosure and field boudary were found on site dated to the 12th to 14th century. post-medeival and modern activity were limited on site. overall, a high density of archaeologicaly significant features were identified during the course of the excavation from a wide range of periods.
    '''
    
    # Czech test (using Polish spaCy language model as Czech not available)
    # https://digiarchiv.aiscr.cz/id/C-201806206A-K02
    cs_test_text1 = '''
    Objekt 2 V severním profilu základového pasu pro rodinný dům byl zachycen objekt konického tvaru s rozšířeným rovným dnem. Parcela: st. p. č. 164 a 165 Souřadnice S-JTSK: 722512/1051371 Nadmořská výška: 333 m n. m. Rozměry: délka 1, 66 m; hloubka 0, 7 m Výplň: Nadloží objektu tvořila cca 30 cm silná vrstva silně hrudkovité velkým množstvím malých kořínků protkané šedé ornice. Horních cca 40 cm výplně objektu tvořila světlešedá až béžově okrová prachovitá hlína promíšená drobnými zlomky mazanice. Spodní cca 30 cm silná část výplně objektu tvořila tmavě šedá až okrová prachová hlína silně promíšená s rozplavenou mazanicí a drobnými zlomky keramiky. Podloží sprašová hlína. Nálezy: keramika 14 zl., mazanice 2 zl., kámen 2 zl. (1x záměrně opracovaný křemen – jádro?) Datovaní: neolit (LnK?), pravěk
    '''
    cs_test_text2 = '''
    Objekt 5 V jižním profilu základového pasu pro rodinný dům byla zachycena část objektu s nepravidelně zahloubeným dnem s pozůstatky ohnišť (dvě uhlíkaté vrstvy na dnech zahloubení). Parcela: ppč. 68/42 Souřadnice S-JTSK: 722398/1051486 Nadmořská výška: 332 m n. m. Rozměry: délka 1, 41 m; hloubka 0, 46 m Výplň: Pod až 28 cm silnou vrstvou ornice tvořené šedohnědou do bločků se rozpadávající jílovité hlíny, zachycena 36 cm silná vrstva šedohnědé jílovité hlíny obsahující zlomky mazanice, kaménků a keramiky. Na dně zahloubení byla zaznamenána 4 až 11 cm silná černá uhlíkatá vrstva. Podloží bylo tvořeno světlehnědými tvrdými jíly. Nálezy: keramika 4 zl., mazanice 5 zl. Datovaní: středověk Objekt 6 Na rozhraní severního a západního profilu základového pasu pro rodinný dům byl zachycen objekt mělce mísovitého tvaru. Parcela: ppč. 68/42 Souřadnice S-JTSK: 722398 /1051485 Nadmořská výška: 332 m n. m. Rozměry: severní profil: délka 0, 74 m; hloubka 0, 51 m, západní profil: délka 1, 95 m; hloubka 0, 51 m Výplň: Pod až 20 cm silnou vrstvou ornice tvořené šedohnědou do bločků se rozpadávající jílovité hlíny, zachycena až 51 cm silná vrstva šedé jílovité hlíny obsahující zlomky keramiky. Podloží bylo tvořeno světlehnědými tvrdými jíly. Nálezy: keramika 6 zl. Datovaní: středověk
    '''
    #nlp = spacy.load("pl_core_news_sm", disable=['ner'])
    #nlp.add_pipe("amcr_ruler", last=True)
    #doc = nlp(cs_test_text2)

    # create pipeline and add one or more custom pipeline components
    nlp = spacy.load("en_core_web_sm", disable=['ner'])

    #nlp = spacy.load("pl_core_news_sm", disable=['ner'])
    #nlp.add_pipe("amcr_ruler", last=True)
    
    # AAT vocabulary pipeline components
    # nlp.add_pipe("aat_activities_ruler", last=True)
    # nlp.add_pipe("aat_agents_ruler", last=True)
    # nlp.add_pipe("aat_associated_concepts_ruler", last=True)
    # nlp.add_pipe("aat_materials_ruler", last=True)
    # nlp.add_pipe("aat_objects_ruler", last=True)
    # nlp.add_pipe("aat_physical_attributes_ruler", last=True)
    # nlp.add_pipe("aat_styleperiods_ruler", last=True)
    # FISH vocabulary pipeline components

    nlp.add_pipe("fish_archobjects_ruler", last=True)
    nlp.add_pipe("fish_monument_types_ruler", last=True)

    #nlp.add_pipe("fish_archsciences_ruler", last=True)
    # nlp.add_pipe("fish_building_materials_ruler", last=True)
    # nlp.add_pipe("fish_components_ruler", last=True)
    # nlp.add_pipe("fish_event_types_ruler", last=True)
    # nlp.add_pipe("fish_evidence_ruler", last=True)
    # nlp.add_pipe("fish_maritime_craft_ruler", last=True)
    # nlp.add_pipe("fish_periods_ruler", last=True)

    doc = nlp(test_text3.lower())
    # explacy.print_parse_info(nlp, test_text.lower())
    # quick and dirty examination of results:
    # for ent in doc.ents:
    # print(ent.ent_id_, ent.text, ent.label_)
    #for tok in doc:
        #print(tok.text, tok.pos_, tok.lemma_)

    # better...
    results = [{
        "from": ent.start_char,
        "to": ent.end_char - 1,
        "id": ent.ent_id_,
        "text": ent.text,
        "type": ent.label_
    } for ent in doc.ents]

    # prevent truncation (of URIs)
    pd.set_option('display.max_colwidth', None)
    # load results into a DataFrame object:    
    df = pd.DataFrame(results)
    print(df)
