"""
=============================================================================
Package :   rematch2
Module  :   VocabularyRuler.py
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy custom pipeline components (specialized SpanRuler)
Imports :   SpanRuler, Language
Example :   N/A - superclass for more specialized components    
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History :   
10/10/2023 CFB Added language factory function
27/10/2023 CFB type hints added for function signatures
28/03/2024 CFB base on SpanRuler instead of EntityRuler
08/01/2024 CFB Moved normalization into create_vocabulary_ruler, 
                added supp_list and stop_list config options
=============================================================================
"""
import spacy
import json
from spacy.pipeline import SpanRuler
from spacy.tokens import Doc
from spacy.language import Language
from pprint import pprint
from pathlib import Path
from spacy import displacy

import pandas as pd

from .spacypatterns import *
from .Util import *
from .DocSummary import DocSummary
from .SpanRemover import child_span_remover
from .BaseRuler import BaseRuler
    

def patterns_from_json_file(file_name: str) -> list:
    base_path = (Path(__file__).parent / "vocabularies").resolve()
    file_path = os.path.join(base_path, file_name)
    patterns = []
    with open(file_path, "r") as f:
        patterns = json.load(f)
        #patterns = list(filter(lambda item: item.get("ignore", False) == False, patterns))

    return patterns


# stop_list is a list of identifiers that should not be matched 
# in order to exclude specific concepts from the match results
@Language.factory(
    name="vocabulary_ruler", 
    default_config = {
        "name": "vocabulary_ruler",
        "spans_key": DEFAULT_SPANS_KEY,
        "default_label": "UNDEFINED",
        "lemmatize": True,
        "min_lemmatize_length": 4,
        "min_term_length": 3,
        "pos": [],
        "patterns": [],         
        "supp_list": [], 
        "stop_list": []
    }
)   
def create_vocabulary_ruler(
        nlp: Language, 
        name: str, 
        spans_key: str = DEFAULT_SPANS_KEY,
        default_label: str = "UNDEFINED",
        lemmatize: bool = True,
        min_lemmatize_length: int = 4,
        min_term_length: int = 3,
        pos: list[str] = [],
        patterns: list[dict] = [],   # list of match patterns
        supp_list: list[dict] = [],  # additional patterns to add to the vocabulary
        stop_list: list[dict] = []   # with identifers not to be matched, to exclude specific concepts from results
    ) -> BaseRuler:

    # create the SpanRuler to use
    ruler = BaseRuler(
        nlp=nlp,        
        name=name,
        spans_key=spans_key,
        phrase_matcher_attr="LOWER",
        validate=False,
        overwrite=False
    )      

    # get normalized patterns    
    normalized_patterns = BaseRuler.normalize_patterns(
        nlp=nlp, 
        patterns=patterns + supp_list,
        default_label=default_label,
        lemmatize=lemmatize,
        min_lemmatize_length=min_lemmatize_length,
        min_term_length=min_term_length,
        pos=pos
    )

    # only include patterns with identifiers that are not in the stop_list
    stop_ids = list(map(lambda item: item.get("id", ""), stop_list))    
    filtered_patterns = [patt for patt in normalized_patterns if patt.get("id", "") not in stop_ids]    
    ruler.add_patterns(filtered_patterns)
    return ruler 


@Language.factory(name="ssh_lcsh_ruler", default_config={"language": "en", "supp_list": [], "stop_list": []})
def create_ssh_lcsh_ruler(
    nlp: Language, 
    name: str, 
    language: str, 
    supp_list: list, 
    stop_list: list
    ) -> BaseRuler:
    
    patterns = patterns_from_json_file("patterns_SSH_LCSH.json")
    clean_language =  language.strip().lower()
    patterns_for_language = list(filter(lambda x: x.language.strip().lower() == clean_language, patterns))
    
    ruler = create_vocabulary_ruler(
        nlp=nlp, 
        name=name, 
        default_label="SSH_LCSH", 
        patterns=patterns_for_language, 
        supp_list=supp_list,
        stop_list=stop_list
    )
    return ruler


@Language.factory(name="amcr_ruler", default_config={"supp_list": [], "stop_list": []})
def create_amcr_ruler(
    nlp: Language, 
    name: str,
    supp_list: list, 
    stop_list: list
    ) -> BaseRuler:
    
    patterns=patterns_from_json_file("patterns_cs_AMCR_20221208.json")
    
    ruler = create_vocabulary_ruler(
        nlp=nlp, 
        name=name, 
        default_label="AMCR", 
        patterns=patterns,
        supp_list=supp_list,
        stop_list=stop_list
    )
    return ruler    
    

@Language.factory(name="aat_activities_ruler", default_config={"supp_list": [], "stop_list": []})
def create_aat_activities_ruler(
    nlp: Language, 
    name: str, 
    supp_list: list, 
    stop_list: list
    ) -> BaseRuler:
    
    patterns=patterns_from_json_file("patterns_en_AAT_ACTIVITIES_20231018.json")
    #patts2=patterns_from_json_file("patterns_en_AAT_ACTIVITIES_SUPPLEMENTARY.json")
   
    ruler = create_vocabulary_ruler(
        nlp=nlp, 
        name=name, 
        default_label="AAT_ACTIVITY", 
        pos=["VERB"],
        patterns=patterns,
        supp_list=supp_list,
        stop_list=stop_list
    )
    return ruler


@Language.factory(name="aat_agents_ruler", default_config={"supp_list": [], "stop_list": []})
def create_aat_agents_ruler(
    nlp: Language, 
    name: str, 
    supp_list: list, 
    stop_list: list
    ) -> BaseRuler:

    patterns=patterns_from_json_file("patterns_en_AAT_AGENTS_20231018.json")
    
    ruler = create_vocabulary_ruler(
        nlp=nlp, 
        name=name, 
        default_label="AAT_AGENT",
        patterns=patterns, 
        pos=["NOUN", "PROPN"],
        supp_list=supp_list,
        stop_list=stop_list
    )
    return ruler
    

@Language.factory(name="aat_associated_concepts_ruler", default_config={"supp_list": [], "stop_list": []})
def create_aat_associated_concepts_ruler(
    nlp: Language, 
    name: str, 
    supp_list: list, 
    stop_list: list
    ) -> BaseRuler:   

    patterns=patterns_from_json_file("patterns_en_AAT_ASSOCIATED_CONCEPTS_20231018.json")
    
    ruler = create_vocabulary_ruler(
        nlp=nlp, 
        name=name, 
        default_label="AAT_ASSOCIATED_CONCEPT", 
        patterns=patterns,
        supp_list=supp_list,
        stop_list=stop_list
    )
    return ruler


@Language.factory(name="aat_materials_ruler", default_config={"supp_list": [], "stop_list": []})
def create_aat_materials_ruler(
    nlp: Language, 
    name: str, 
    supp_list: list, 
    stop_list: list
    ) -> BaseRuler:   

    patterns=patterns_from_json_file("patterns_en_AAT_MATERIALS_20231018.json")
    
    ruler = create_vocabulary_ruler(
        nlp=nlp, 
        name=name, 
        default_label="AAT_MATERIAL", 
        patterns=patterns,
        supp_list=supp_list,
        stop_list=stop_list
    )
    return ruler


@Language.factory(name="aat_objects_ruler", default_config={"supp_list": [], "stop_list": []})
def create_aat_objects_ruler(
    nlp: Language, 
    name: str, 
    supp_list: list,
    stop_list: list
    ) -> BaseRuler:

    patterns=patterns_from_json_file("patterns_en_AAT_OBJECTS_20231018.json")
        
    ruler = create_vocabulary_ruler(
        nlp=nlp, 
        name=name, 
        default_label="AAT_OBJECT", 
        pos=["NOUN", "PROPN"], 
        patterns=patterns,
        supp_list=supp_list,
        stop_list=stop_list
    )
    return ruler


@Language.factory(name="aat_physical_attributes_ruler", default_config={"supp_list": [], "stop_list": []})
def create_aat_physical_attributes_ruler(
    nlp: Language, 
    name: str, 
    supp_list: list,
    stop_list: list
    ) -> BaseRuler: 

    patterns=patterns_from_json_file("patterns_en_AAT_PHYSICAL_ATTRIBUTES_20231018.json")
    
    ruler = create_vocabulary_ruler(
        nlp=nlp, 
        name=name, 
        default_label="AAT_PHYSICAL_ATTRIBUTE", 
        patterns=patterns,
        supp_list=supp_list,
        stop_list=stop_list
    )
    return ruler


@Language.factory(name="aat_styleperiods_ruler", default_config={"supp_list": [], "stop_list": []})
def create_aat_styleperiods_ruler(
    nlp: Language, 
    name: str, 
    supp_list: list,
    stop_list: list
    ) -> BaseRuler: 

    patterns=patterns_from_json_file("patterns_en_AAT_STYLEPERIODS_20231018.json")
    
    ruler = create_vocabulary_ruler(
        nlp=nlp, 
        name=name, 
        default_label="AAT_STYLEPERIOD", 
        patterns=patterns,
        supp_list=supp_list, 
        stop_list=stop_list
    )
    return ruler


@Language.factory("fish_archobjects_ruler", default_config={"supp_list": [], "stop_list": []})
def create_fish_archobjects_ruler(
    nlp: Language, 
    name: str, 
    supp_list: list,
    stop_list: list
    ) -> BaseRuler: 

    patterns = patterns_from_json_file("patterns_en_FISH_ARCHOBJECTS_20210921.json")
    
    ruler = create_vocabulary_ruler(
        nlp=nlp, 
        name=name, 
        default_label="FISH_OBJECT", 
        pos=["NOUN"],  
        min_lemmatize_length=3,
        patterns=patterns,
        supp_list=supp_list, 
        stop_list=stop_list
    )
    return ruler


@Language.factory(name="fish_archsciences_ruler", default_config={"supp_list": [], "stop_list": []})
def create_fish_archsciences_ruler(
    nlp: Language, 
    name: str, 
    supp_list: list,
    stop_list: list
    ) -> BaseRuler: 

    patterns=patterns_from_json_file("patterns_en_FISH_ARCHSCIENCES_20210921.json")
   
    ruler = create_vocabulary_ruler(
        nlp=nlp, 
        name=name, 
        default_label="FISH_ARCHSCIENCE", 
        pos=["VERB"], 
        patterns=patterns,
        supp_list=supp_list,
        stop_list=stop_list
    )
    return ruler


@Language.factory(name="fish_building_materials_ruler", default_config={"supp_list": [], "stop_list": []})
def create_fish_building_materials_ruler(
    nlp: Language, 
    name: str, 
    supp_list: list,
    stop_list: list
    ) -> BaseRuler:  

    patterns=patterns_from_json_file("patterns_en_FISH_BUILDING_MATERIALS_20210921.json")
    
    ruler = create_vocabulary_ruler(
        nlp=nlp, 
        name=name, 
        default_label="FISH_MATERIAL", 
        patterns=patterns,
        supp_list=supp_list, 
        stop_list=stop_list
    )
    return ruler


@Language.factory(name="fish_components_ruler", default_config={"supp_list": [], "stop_list": []})
def create_fish_components_ruler(
    nlp: Language, 
    name: str, 
    supp_list: list,
    stop_list: list
    ) -> BaseRuler:

    patterns=patterns_from_json_file("patterns_en_FISH_COMPONENTS_20210921.json")
    
    ruler = create_vocabulary_ruler(
        nlp=nlp, 
        name=name, 
        default_label="FISH_OBJECT", 
        pos=["NOUN"], 
        patterns=patterns,
        supp_list=supp_list, 
        stop_list=stop_list
    )
    return ruler


@Language.factory(name="fish_event_types_ruler", default_config={"supp_list": [], "stop_list": []})
def create_fish_event_types_ruler(
    nlp: Language, 
    name: str, 
    supp_list: list,
    stop_list: list
    ) -> BaseRuler:    

    patterns=patterns_from_json_file("patterns_en_FISH_EVENT_TYPES_20210921.json")
    
    ruler = create_vocabulary_ruler(
        nlp=nlp, 
        name=name, 
        default_label="FISH_EVENT", 
        pos=["VERB"], 
        patterns=patterns,
        supp_list=supp_list, 
        stop_list=stop_list
    )
    return ruler


@Language.factory("fish_evidence_ruler", default_config={"supp_list": [], "stop_list": []})
def create_fish_evidence_ruler(
    nlp: Language, 
    name: str, 
    supp_list: list,
    stop_list: list
    ) -> BaseRuler: 

    patterns=patterns_from_json_file("patterns_en_FISH_EVIDENCE_20210921.json")
    
    ruler = create_vocabulary_ruler(
        nlp=nlp, 
        name=name, 
        default_label="FISH_EVIDENCE", 
        patterns=patterns, 
        supp_list=supp_list,
        stop_list=stop_list
    )
    return ruler


@Language.factory(name="fish_maritime_craft_ruler", default_config={"supp_list": [], "stop_list": []})
def create_fish_maritime_craft_ruler(
    nlp: Language, 
    name: str, 
    supp_list: list,
    stop_list: list
    ) -> BaseRuler: 

    patterns=patterns_from_json_file("patterns_en_FISH_MARITIME_CRAFT_20221104.json")
    
    ruler = create_vocabulary_ruler(
        nlp=nlp, 
        name=name, 
        default_label="FISH_OBJECT", 
        pos=["NOUN"], 
        patterns=patterns,
        supp_list=supp_list, 
        stop_list=stop_list
    )
    return ruler


@Language.factory(name="fish_monument_types_ruler", default_config={"supp_list": [], "stop_list": []})
def create_fish_monument_types_ruler(
    nlp: Language, 
    name: str, 
    supp_list: list,
    stop_list: list
    ) -> BaseRuler:
    
    patterns = patterns_from_json_file("patterns_en_FISH_MONUMENT_TYPES_20210921.json")
    #patts2 = patterns_from_json_file("patterns_en_FISH_MONUMENT_TYPES_SUPPLEMENTARY.json")
        
    ruler = create_vocabulary_ruler(
        nlp=nlp, 
        name=name, 
        default_label="FISH_MONUMENT", 
        pos=["NOUN"], 
        min_lemmatize_length=3, 
        patterns=patterns,
        supp_list=supp_list,
        stop_list=stop_list
    )
    return ruler


@Language.factory(name="fish_periods_ruler", default_config={"supp_list": [], "stop_list": []})
def create_fish_periods_ruler(
    nlp: Language, 
    name: str, 
    supp_list: list,
    stop_list: list
    ) -> BaseRuler:  

    patterns=patterns_from_json_file("patterns_en_FISH_PERIODS_20211011.json")
    
    ruler = create_vocabulary_ruler(
        nlp=nlp, 
        name=name, 
        default_label="FISH_PERIOD", 
        patterns=patterns,
        supp_list=supp_list,
        stop_list=stop_list
    )
    return ruler


@Language.factory(name="fish_supplementary_ruler", default_config={"supp_list": [], "stop_list": []})
def create_fish_supplementary_ruler(
    nlp: Language, 
    name: str, 
    supp_list: list,
    stop_list: list
    ) -> BaseRuler:    

    patterns=patterns_from_json_file("patterns_en_FISH_SUPPLEMENTARY.json")
    
    ruler = create_vocabulary_ruler(
        nlp=nlp, 
        name=name, 
        default_label="FISH_OBJECT", 
        patterns=patterns,
        supp_list=supp_list, 
        stop_list=stop_list
    )
    return ruler


# test the BaseRuler class
if __name__ == "__main__":

    # sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    # from rematch2.spacypatterns import vocab_en_AAT_OBJECTS
    # from ..spacypatterns import vocab_en_AAT_OBJECTS

    en_test_text1 = '''Aside from three residual flints, none closely datable, the earliest remains from the archeomagnetism comprised a small assemblage of Roman pottery and Lower Paleolithic or Lower Palaeolithic ceramic building material, also residual and most likely derived from a Roman farmstead found immediately to the north within the Phase II excavation area. A single sherd of Anglo-Saxon grass-tempered pottery was also residual. The earliest features, which accounted for the majority of the remains on site, relate to medieval agricultural activity focused within a large enclosure. There was little to suggest domestic occupation within the site: the pottery assemblage was modest and well abraded, whilst charred plant remains were sparse, and, as with some metallurgical residues, point to waste disposal rather than the locations of processing or consumption. A focus of occupation within the Rodley Manor site, on higher ground 160m to the north-west, seems likely, with the currently site having lain beyond this and providing agricultural facilities, most likely corrals and pens for livestock. Animal bone was absent, but the damp, low-lying ground would have been best suited to cattle. An assemblage of medieval coins recovered from the subsoil during a metal detector survey may represent a dispersed hoard.'''
    en_test_text2 = '''
    mola conducted an archaeological desk-based heritage assessment including radiocarbon dating of land at fakenham road, great ryburgh, norfolk. the earliest archaeological evidence found dates from the mesolithic period. neolithic flint tools have been found close to the west and north-west of the site. a possible bronze age ring ditch has been identified to the north-east and finds dating to the period have been discovered through metal detecting surveys. iron age remains including pits and pottery have been found within the area of proposed development through trial trenching. the site lies between two roman settlements on the south-western banks of the river wensum. one lies nearby to the north-west of the site and numerous finds including coins have been discovered during a fieldwalking survey. a further roman settlement lies to the south-east where two enclosures, two kilns and two burials have recently been excavated. a middle saxon cemetery, drainage ditches, an enclosure, land divisions and a substantial boundary ditch have also recently been discovered to the south-east of the site. metal finds dating to the period have also been found to the north-west and to the east of the site during metal detecting surveys. the site lies beyond the historic core of great ryburgh. the medieval settlement developed around the junction of fakenham road and bridge road to the west of the river wensum, flanked by the medieval moated manor of ryburgh at the northern end and by st andrew's church to the south. cartographic evidence suggests that the site lay to the rear of properties fronting fakenham road during the post-medieval period and had remained as undeveloped farmland.'''
    en_test_text3 = '''
    The Excavation revealed a wealth of archaeological information. The earliest period was represented by residual finds of a Mesolithic worked flint axe in a medieval plough furrow and Bronze Age aurochs bone in an Iron Age pit. The Iron Age period consisted of several phases of a Banjo Enclosure with associated roundhouses, four-post structures, boundary ditches, pits and a quarry. In the early Roman period there was little activity other than quarrying, but later a farmstead was established with an agricultural system reminiscent of a vineyard. No evidence was recovered for the Saxon period, even as residual finds in later contexts, and thus it is assumed that the site was either unused by the population at that time, or subject to a regime that has left no trace in the archaeological record. In the medieval period a ridge and furrow cultivation system was established that cut across many earlier features but incorporated surprisingly little material from earlier periods. After the medieval period, the site appears to have been largely abandoned until Enclosure. The two phases of work took place between March - May 2000 and subsequently between August - October 2001 by CAM ARC, Cambridgeshire County Council (formerly the Archaeological Field Unit).
    '''
    en_test_text4 = '''
    in autumn 2008 a programme of archaeological excavation was undertaken  at titnore lane, goring-by-sea.  the excavation was conducted across the full area of the 2.2 hectare site.    a wide range of periods were represented on site, incorporating the mesolithic, neolithic, bronze age, iron age, romano-british, medieval, and later post-medeival activity. the features and finds assemblage associated with the mesolithic and neolithic were limited, representing only a periodic use of the site. the key feature associated with mid to late bronze age activity was a c.3.5m wide trackway identified as running north-south across the site. by the late bronze age/early iron age period the first evidence of settlement was identified, formed of a roundhouse, pits and a possible livestock corral. the mid to late iron age period saw a growth in settlement with several phases of roundhouse construction associated with boundary ditches, pitting, further possible corrals and  the creation of an artificial pond adjacent to the settlement. the settlement had disappeared by the 1st century ad replaced by a series of field boundaries and rubbish pits thought to part of the villa complex known immediately to the south of the site. romano-british activity did not survive beyond the early to mid 2nd century. a large enclosure and field boudary were found on site dated to the 12th to 14th century. post-medeival and modern activity were limited on site. overall, a high density of archaeologicaly significant features were identified during the course of the excavation from a wide range of periods.
    '''
    en_test_text5 = '''
    During the burial ground survey, evidence of a late Roman fort was located near the earlier Neolithic flint knapping site. Fragments of a roofing nail were found.
    '''
    en_test_text6 = '''
    An archaeological excavation on land at Riverside (East of Steamer Quay Road), Totnes,  Devon (SX 8104 5981), was undertaken by AC archaeology during September 2014 and July 2015. Three areas were excavated centred on a series archaeological features identified  during previous trial trenching. Evidence for background prehistoric activity dating from the Mesolithic through to the Early  Bronze Age was identified. No in situ features were securely dated to this period, although a  number of natural tree throws could be associated with this phase of activity. A pit furnace for  iron working excavated during the earlier trial trenching has subsequently been radiocarbon  dated to the 4th-6th centuries AD. Evidence for limited agricultural activity dating from the  Romano-British through to the modern period was also recorded. Finds recovered comprise  small quantities of pottery dating from the prehistoric through to the post-medieval period,  several metal objects, ceramic building material, glass, clay tobacco pipe and prehistoric  worked flint, including a barbed and tanged arrowhead.
    '''

    # Czech test (using Polish spaCy language model as Czech not available)
    # https://digiarchiv.aiscr.cz/id/C-201806206A-K02
    cs_test_text1 = '''
    Objekt 2 V severním profilu základového pasu pro rodinný dům byl zachycen objekt konického tvaru s rozšířeným rovným dnem. Parcela: st. p. č. 164 a 165 Souřadnice S-JTSK: 722512/1051371 Nadmořská výška: 333 m n. m. Rozměry: délka 1, 66 m; hloubka 0, 7 m Výplň: Nadloží objektu tvořila cca 30 cm silná vrstva silně hrudkovité velkým množstvím malých kořínků protkané šedé ornice. Horních cca 40 cm výplně objektu tvořila světlešedá až béžově okrová prachovitá hlína promíšená drobnými zlomky mazanice. Spodní cca 30 cm silná část výplně objektu tvořila tmavě šedá až okrová prachová hlína silně promíšená s rozplavenou mazanicí a drobnými zlomky keramiky. Podloží sprašová hlína. Nálezy: keramika 14 zl., mazanice 2 zl., kámen 2 zl. (1x záměrně opracovaný křemen – jádro?) Datovaní: neolit (LnK?), pravěk
    '''
    cs_test_text2 = '''
    Objekt 5 V jižním profilu základového pasu pro rodinný dům byla zachycena část objektu s nepravidelně zahloubeným dnem s pozůstatky ohnišť (dvě uhlíkaté vrstvy na dnech zahloubení). Parcela: ppč. 68/42 Souřadnice S-JTSK: 722398/1051486 Nadmořská výška: 332 m n. m. Rozměry: délka 1, 41 m; hloubka 0, 46 m Výplň: Pod až 28 cm silnou vrstvou ornice tvořené šedohnědou do bločků se rozpadávající jílovité hlíny, zachycena 36 cm silná vrstva šedohnědé jílovité hlíny obsahující zlomky mazanice, kaménků a keramiky. Na dně zahloubení byla zaznamenána 4 až 11 cm silná černá uhlíkatá vrstva. Podloží bylo tvořeno světlehnědými tvrdými jíly. Nálezy: keramika 4 zl., mazanice 5 zl. Datovaní: středověk Objekt 6 Na rozhraní severního a západního profilu základového pasu pro rodinný dům byl zachycen objekt mělce mísovitého tvaru. Parcela: ppč. 68/42 Souřadnice S-JTSK: 722398 /1051485 Nadmořská výška: 332 m n. m. Rozměry: severní profil: délka 0, 74 m; hloubka 0, 51 m, západní profil: délka 1, 95 m; hloubka 0, 51 m Výplň: Pod až 20 cm silnou vrstvou ornice tvořené šedohnědou do bločků se rozpadávající jílovité hlíny, zachycena až 51 cm silná vrstva šedé jílovité hlíny obsahující zlomky keramiky. Podloží bylo tvořeno světlehnědými tvrdými jíly. Nálezy: keramika 6 zl. Datovaní: středověk
    '''
    cs_test_text3 = '''
    Objekt zámku v Chanovicích (okr. Klatovy) se nalézá spolu s pozdně románským
kostelem sv. Kříže na severozápadním okraji obce. Byl postaven na nevýrazné ostrožně, jejíž
páteř vytvářejí výchozy žulové skály. Ze tří stran sídlo obklopuje zpustlý park s rybníkem
v jeho dolní části. Na severovýchodní straně pak k zámku přiléhá areál hospodářského dvora.
Nejstarším dokladem existence chanovického sídla je pozdně románský kostel Povýšení
sv. Kříže. Jako vlastnický kostel se patrně vázal na zde již existující feudální sídlo.
Předpokládá se, že leželo v místech pozdějšího poplužního dvora, dnes dochovaného
v klasicistní přestavbě. V průběhu 13. stol. bylo sídlo přeneseno na skalnatou ostrožnu, do
míst dnešního zámku.
V písemných pramenech se Chanovice objevují ve 2. polovině 14. století. Z této doby
pochází též nejstarší dochovaná gotická část sídla. K výrazné přestavbě objektu došlo v
prvních desetiletích 16. století za Chanovských z Dlouhé Vsi, kdy stavba nabyla dnešní
půdorysné podoby. Areál byl ohrazen novou, značně silnou obvodovou zdí, respektující v
některých úsecích starší konstrukce. Roku 1670 byla Chanovicím odpuštěna část berní
povinnosti, což snad naznačuje, že obec v této době postihla jakási živelná pohroma.
Do podoby sídla výrazně zasáhla barokní přestavba, ke které došlo někdy okolo
poloviny 18. století za majitele Ferdinanda Jáchyma Rumerskirchena. Dílčí zásahy do stavby
nastaly patrně také po ničivém požáru roku 1781, při kterém vyhořel kostel, fara, škola a
zámek spolu s hospodářskými budovami přilehlého dvora.
Na přelomu 18. a 19. stol. zámek rychle střídal majitele a pustnul. Písemné prameny
uvádí, že roku 1811 objekt, v té době ve velmi špatném stavu, koupil plzeňský podnikatel
František Becher. Ten nechal sejmout jedno patro, zámek opravil a pokryl těžkou krytinou.
Úpravám se nevyhnul ani chanovický hospodářský dvůr. Částečně ho nechal přestavět na
konci 19. stol. nový majitel Eduard Rytíř z Doubků. Poslední známá úprava hospodářského
dvora byla projekčně připravována v roce 1901. (Anderle – Ebel 1996)
    '''
    #nlp = spacy.load("pl_core_news_sm", disable=['ner'])
    #nlp.add_pipe("amcr_ruler", last=True)
    #doc = nlp(cs_test_text2)

    # create pipeline and add one or more custom pipeline components

    nlp = get_pipeline_for_language("en")
    #nlp = spacy.load("pl_core_news_sm", disable=['ner'])
    #nlp.add_pipe("amcr_ruler", last=True)
    
    # AAT vocabulary pipeline components
    #nlp.add_pipe("normalize_text", before = "tagger")
    nlp.add_pipe("aat_activities_ruler", last=True)
    # nlp.add_pipe("aat_agents_ruler", last=True)
    # nlp.add_pipe("aat_associated_concepts_ruler", last=True)
    # nlp.add_pipe("aat_materials_ruler", last=True)
    # nlp.add_pipe("aat_objects_ruler", last=True)
    # nlp.add_pipe("aat_physical_attributes_ruler", last=True)
    # nlp.add_pipe("aat_styleperiods_ruler", last=True)
    # FISH vocabulary pipeline components

    #nlp.add_pipe("fish_archobjects_ruler", last=True)
    # testing monuments ruler with use of stop_list e.g. removing concept 'site' from patterns so we don't get matches on it in results
    #nlp.add_pipe("fish_monument_types_ruler", last=True, config={ "stop_list": ["http://purl.org/heritagedata/schemes/eh_tmt2/concepts/70412"] })
    #nlp.add_pipe("respeller", before="tagger")
    #nlp.add_pipe("fish_archsciences_ruler", last=True)
    #nlp.add_pipe("fish_building_materials_ruler", last=True)
    # nlp.add_pipe("fish_components_ruler", last=True)
    #nlp.add_pipe("fish_event_types_ruler", last=True)
    # nlp.add_pipe("fish_evidence_ruler", last=True)
    # nlp.add_pipe("fish_maritime_craft_ruler", last=True)
    #nlp.add_pipe("fish_periods_ruler", last=True)
    #nlp.add_pipe("child_span_remover", last=True) 

    doc = nlp(en_test_text2)
    # explacy.print_parse_info(nlp, en_test_text.lower())
    print("Tokens:\n" + DocSummary(doc).tokens_to_text())
    print("Spans:\n" + DocSummary(doc).spans_to_text())

    options = {
        "spans_key": DEFAULT_SPANS_KEY,
        "colors": {
            "DATEPREFIX": "lightgray",
            "FISH_OBJECT": "plum",
            "FISH_MONUMENT": "lightblue",
            "FISH_ARCHSCIENCE": "lightpink",
            "AAT_ACTIVITY": "lightsalmon",
            "FISH_EVIDENCE": "aliceblue",
            "FISH_MATERIAL": "antiquewhite",
            "FISH_EVENT": "coral",
            "FISH_PERIOD": "yellow"
        }
    }
    displacy.serve(doc, style="span", options=options, auto_select_port=True)
