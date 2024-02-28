"""
=============================================================================
Package :   rematch2
Module  :   NegationRuler.py
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy custom pipeline component (specialized EntityRuler)
            Language-sensitive component to identify negation phrases
            in free text. Entity type added will be "NEGATION"
Imports :   os, sys, spacy, Language, EntityRuler, Doc
Example :   nlp.add_pipe("negation_ruler", last=True)           
License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History :   
28/02/2024 CFB Initially created script
=============================================================================
"""
import os
import sys
import spacy            # NLP library
from spacy.pipeline import EntityRuler

from spacy.language import Language
from spacy.lang.en import English

if __package__ is None or __package__ == '':
    # uses current directory visibility
    from spacypatterns import *
    from Util import *
else:
    # uses current package visibility
    from .spacypatterns import *
    from .Util import *


@Language.factory("negation_ruler", default_config={"patterns": []})
def create_negation_ruler(nlp: Language, name: str="negation_ruler", patterns: list=[]) -> EntityRuler:
    normalized_patterns = normalize_patterns(
        nlp=nlp, 
        patterns=patterns,
        default_label="NEGATION",
        lemmatize=False,
        min_term_length=3
    )
    return EntityRuler(
        nlp=nlp, 
        name=name, 
        patterns=normalized_patterns,
        phrase_matcher_attr="LOWER",
        validate=False,
        overwrite_ents=True,
        ent_id_sep="||"
    )
    

@English.factory("negation_ruler")
def create_negation_ruler_en(nlp: Language, name: str = "negation_ruler") -> EntityRuler:
    return create_negation_ruler(nlp, name, patterns_en_NEGATION)

'''
@Spanish.factory("negation_ruler")
def create_negation_ruler_es(nlp: Language, name: str = "negation_ruler") -> EntityRuler:
    return create_negation_ruler(nlp, name, patterns_es_NEGATION)


@French.factory("negation_ruler")
def create_negation_ruler_fr(nlp: Language, name: str = "negation_ruler") -> EntityRuler:
    return create_negation_ruler(nlp, name, patterns_fr_NEGATION)


@Italian.factory("negation_ruler")
def create_negation_ruler_it(nlp: Language, name: str = "negation_ruler") -> EntityRuler:
    return create_negation_ruler(nlp, name, patterns_it_NEGATION)


@Dutch.factory("negation_ruler")
def create_negation_ruler_nl(nlp: Language, name: str = "negation_ruler") -> EntityRuler:
    return create_negation_ruler(nlp, name, patterns_nl_NEGATION)


@Norwegian.factory("negation_ruler")
def create_negation_ruler_no(nlp: Language, name: str = "negation_ruler") -> EntityRuler:
    return create_negation_ruler(nlp, name, patterns_no_NEGATION)


@Swedish.factory("negation_ruler")
def create_negation_ruler_sv(nlp: Language, name: str = "negation_ruler") -> EntityRuler:
    return create_negation_ruler(nlp, name, patterns_sv_NEGATION)

# Polish as temp experimental substitute until Czech is available
@Polish.factory("negation_ruler")
def create_negation_ruler_cs(nlp: Language, name: str = "negation_ruler") -> EntityRuler:
    return create_negation_ruler(nlp, name, patterns_cs_NEGATION)
'''

# test the NegationRuler class
if __name__ == "__main__":

    tests = [
        #{"lang": "de", "pipe": "de_core_news_sm",
        #    "text": "Im Januar oder im März oder im Oktober, vielleicht im Dezember?"},
        {"lang": "en", "pipe": "en_core_web_sm",
            "text": "This collection comprises images, reports, spreadsheets, databases, GIS data and site records from three phases of archaeological evaluation at Foxbridge, Swindon, Wiltshire. Work was undertaken by Oxford Archaeology between October 2019 and October 2020. Phase 1 Between 28th October and 8th November 2019, Oxford Archaeology undertook a trial trench evaluation on the site of a proposed mixed development at Foxbridge, Swindon. The works comprised the excavation of 30 trenches and formed the first of three phases of evaluation undertaken within the proposed development area. The 30 trenches were located in the northern half of the proposed development area and included five trenches targeted on geophysical anomalies provisionally interpreted as the continuation of Durocornovium Roman Town, a Scheduled Monument located to the north of and partially within the site. Archaeological remains consistent with Roman roadside activity were identified within these five trenches. It is the intention to preserve this remains in situ and given poor ground conditions during the works, excavation of the exposed features was minimally intrusive. The remains comprised rectilinear enclosures, pits and a couple of postholes but no evidence for in situ structural remains was identified. The activity is contained within a 50m wide strip that runs parallel to the Wanborough Road, which forms the eastern site boundary, and is delimited to the west by a large enclosure ditch. Features of potential archaeological origin investigated to the west of this ditch were demonstrated to be of geological origin. The finds assemblage comprises 396 sherds of Roman pottery, ceramic building material, glass and metal objects, worked flint, animal bone and stone. The assemblage suggests the activity within the site occurred predominately in the middle Roman period with none of the contexts dated to earlier than the 2nd century. The pottery assemblage, however, does contain sherds dating to the late Roman period suggesting activity within the site continued into the 4th and early 5th centuries. This is supported by the metalwork assemblage which includes six late Roman coins. Although no obvious in situ building remains were present, several fragments of roof tile and unworked limestone were recovered and suggest the presence of structures within the vicinity. Similarly, the recovery of metal working slag suggests industrial activities occurred within the area, but no evidence was recorded within the trenches. A single inhumation was identified, and although heavily disturbed it is believed to be that of an adult male. A buried soil of unknown origin was recorded sealing the archaeological features. The origin of this deposit is uncertain, but it is suspected to represent a former land surface or occupation layer. No archaeological features or deposit were recorded in the trenches located beyond those targeting the roadside activity.  Phase 2 In August 2020, Oxford Archaeology undertook a trial-trench evaluation at the site of a proposed mixed development. The works comprised the excavation of seven trenches within the scheduled area of the Roman town of Durocornovium. Although evenly distributed across the site, several of the trenches were positioned to investigate anomalies identified by geophysical survey. The correlation between geophysical anomalies and the features exposed during the evaluation was poor. Despite this, the evaluation identified a concentration of middle and late Roman activity. Wanbrough Road, which forms the eastern site boundary, follows the route of the Roman road of Ermin street. The distribution of features within the site suggests a focus of activity along the roadside. Beam slots indicate the presence of a wooden structure dating to the middle Roman period, and three stone walls form a multi-phased, multi-roomed building of unknown function. Ditches forming a rectangular enclosure and possible trackways were also present. Pottery recovered from the features suggest they originated in the middle Roman period. Many of the ditches appear to have been maintained or re-established, and artefactual evidence suggest several continued in use into the late Roman period. Further away from Ermin street, in the south-west corner of the site, the remains of a small cemetery were exposed. Eight inhumation burials were identified and extending beyond the limits of one of the trenches. The extent of the cemetery is unknown, but the southern limit appears to be defined by a small gully. The finds assemblage comprised 827 sherds of Roman pottery, the majority of which dates to the late Roman period, as well as glass, metal objects including coins, and animal bones.  Phase 3 In late September and early October 2020, Oxford Archaeology undertook a trial-trench evaluation at Foxbridge, Swindon, the site of a proposed mixed development. The works comprised the excavation of 29 trenches and is the third phase of evaluation undertaken within the site. Due to prolong heavy rain the trenches became waterlogged during the evaluation. While it is not considered that these conditions hindered the identification of archaeological remains within the trenches, it did impact the level of hand excavation that could be undertaken and therefore the characterisation of several features identified. Archaeological features dating from the late Mesolithic/early Neolithic period through to the post-medieval period were recorded across the area. The archaeological features were distributed across the site and predominately comprised ditches and a number of pits. The trenches were positioned to ground truth the results of a geophysical survey. The correlation between the results of the survey and the trial trenching is mixed. Geophysical anomalies interpreted as 'positive linear archaeology' were all present and were dated to the medieval and postmedieval periods. However, the correlation between anomalies interpreted with less certainty was moderately poor. While some archaeological features were identified that correlated with the anomalies, there was no evidence for others. Several archaeological features were also identified during the evaluation that were not identified by the geophysical survey. The earliest activity recorded comprises an assemblage of struck flint from an alluvial deposit in the centre of the site. The assemblage includes blade cores and debitage indicative of blade production dating to the early Neolithic period, although a late Mesolithic date is possible. Although the assemblage was not recovered from an in situ scatter, the struck flint is fresh and is unlikely to have been moved far from the original point of deposition, suggesting flint production within the site. A small prehistoric enclosure was also identified. The absence of internal features suggest it served an agricultural function as a stock enclosure, rather than being indicative of domestic/settlement activity. Pottery recovered from the feature has been dated to the mid to late Bronze Age and the early to middle Iron Age. Prehistoric pottery was also recovered from a number of ditches. Previous evaluations within the Foxbridge site have identified significant activity of Roman date associated with Wanborough Roman town, which lies to the north. Only four land management ditches of Roman date were recorded during this phase of evaluation. Dated to the 1st and 2nd centuries, the ditches are more likely to be associated with an early Roman farmstead located 300m to the south-west of the site than with the activity recorded during the previous phases of evaluation within the Foxbridge site which is predominately of middle and late Roman date. The Phase 3 area appears to lie between the two foci of Roman activity. The ditches dating to both the prehistoric and Roman periods represent land management and drainage, but it is not possible to define any field systems based on their orientation and distribution.   Enclosure ditches most likely associated with a small medieval/post-medieval farmstead were also recorded within the site."},
        #{"lang": "es", "pipe": "es_core_news_sm",
        #    "text": "¿En enero o en marzo o en octubre, tal vez en diciembre?"},
        #{"lang": "fr", "pipe": "fr_core_news_sm",
        #    "text": "En janvier ou en mars ou en octobre, peut-être en décembre?"},
        #{"lang": "it", "pipe": "it_core_news_sm",
        #    "text": "A gennaio o a marzo o a ottobre, forse a dicembre?"},
        #{"lang": "nl", "pipe": "nl_core_news_sm",
        #    "text": "In januari of in maart of in oktober, misschien in december?"},
        #{"lang": "no", "pipe": "nb_core_news_sm",
         #   "text": "I januar eller i mars eller i oktober, kanskje i desember?"},
        #{"lang": "sv", "pipe": "sv_core_news_sm",
         #   "text": "I januari eller i mars eller i oktober, kanske i december?"}
    ]
    for test in tests:
        print(f"-------------\nlanguage = {test['lang']}")
        nlp = spacy.load(test["pipe"], disable=['ner'])
        nlp.add_pipe("negation_ruler", last=True)
        doc = nlp(test["text"])
        for ent in doc.ents:
            print(ent.ent_id_, ent.text, ent.label_)
