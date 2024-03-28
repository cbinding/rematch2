"""
=============================================================================
Package :   rematch2
Module  :   PeriodoRuler.py
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   
Summary :   spaCy custom pipeline component (specialized EntityRuler) to 
            identify named periods (from Perio.do) in free text. 
            Entity type added will be "PERIOD"
Imports :   os, sys, spacy, Language, EntityRuler, Doc, Language
Example :   
        nlp = spacy.load(pipe_name, disable=['ner'])
        nlp.add_pipe("periodo_ruler", last=True) 
        doc = nlp(test_text)

License :   https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
=============================================================================
History :   
03/08/2022 CFB Initially created script
27/10/2023 CFB type hints added for function signatures
16/02/2024 CFB removed BaseRuler inheritance, use EntityRuler directly
               renamed to PeriodoRuler, and "NAMEDPERIOD" => "PERIOD"
=============================================================================
"""
import os
import sys
import spacy            # NLP library
import pandas as pd
from spacy.pipeline import SpanRuler
from spacy.tokens import Doc
from spacy.language import Language

if __package__ is None or __package__ == '':
    # uses current directory visibility
    from PeriodoData import PeriodoData
    from Util import *
    from DocSummary import DocSummary
else:
    # uses current package visibility
    from .PeriodoData import PeriodoData
    from .Util import *
    from .DocSummary import DocSummary


@Language.factory(name="periodo_ruler", default_config={"periodo_authority_id": None})
def create_periodo_ruler(nlp: Language, name: str="periodo_ruler", periodo_authority_id: str="") -> SpanRuler:
    # get terms from selected Perio.do authority as vocab
    # get as new instance, don't refresh cached data
    pd = PeriodoData(from_cache=True) #tmp...

    # get periods for authority id
    periods = pd.get_period_list(periodo_authority_id)

    # parse out and convert  
    patterns = list(map(lambda item: {
        "id": item.get("uri", ""),
        "label": "PERIOD",
        "pattern": item.get("label", "")
    }, periods or []))

    normalized_patterns = normalize_patterns(
        nlp=nlp, 
        patterns=patterns,
        default_label="PERIOD",
        lemmatize=False
    )

    ruler = SpanRuler(
        nlp=nlp,        
        name=name,
        spans_key="custom",
        phrase_matcher_attr="LOWER",
        validate=False,
        overwrite=False
    )  
      
    ruler.add_patterns(normalized_patterns)
    return ruler 
  

# test the PeriodoRuler class
if __name__ == "__main__":

    # import json
    # from ..test_examples import test_examples
    # test_file_name = "test_examples.py"
    # tests = []
    # with open(test_file_name, "r") as f:  # what if file doesn't exist?
    # tests = json.load(f)

    pipeline = "fr_core_news_sm"
    periodo_authority_id = "p02chr4"
    test_text = '''Quelques éléments lithiques Würm IV dispersés sont des indicateurs de la période néolithique d'environ fin 11000 - début 10000 av JC. 
    Un ensemble de fosses, circonscrit sur une surface de 35 m2, a livré du mobilier céramique du premier âge du Fer (Hallstatt C) et quelques éléments lithiques. 
    Un bâtiment sur poteaux se situe à une distance de 100 m vers l’ouest. 
    Pour la période de La Tène finale et gallo-romaine, l’ensemble des vestiges fossoyés et bâtis sont concentrés sur une parcelle à la croisée de deux chemins actuels présents sur le cadastre de 1807. 
    L’élément structurant majeur est le fossé F6 qui traverse perpendiculairement la parcelle, large de 3 m pour une profondeur de 1,80 m sous la terre arable. 
    Seul un angle de fossé, de nature différente et de plus petite taille, semble participer à cette même organisation du paysage. 
    Un bâtiment de plan rectangulaire, 13 x 9 m, sur fondations de schiste dont deux angles ont été découverts, est orienté de façon identique au fossé F6. 
    Il est très bien fondé sur une profondeur de 0,70 m avec de gros blocs de schiste. 
    Si quelques rares tessons du Haut-Empire ont été trouvés dans la fondation du bâtiment, le mobilier céramique du colmatage de la zone humide située à 10 m au sud-ouest, est compris entre le milieu du Ier siècle et le début du IIe siècle de notre ère. 
    Situé à 45 m plus au sud et parallèle au bâtiment, un fossé rectiligne de 3 m de large pour 1,80 m de profondeur sous la terre arable, scinde l’espace en deux. 
    Son creusement en V à été comblé en deux temps. 
    La première phase est une sédimentation naturelle qui a piégé quelques tessons protohistoriques et des scories ferreuses dont un culot de forge. 
    Le colmatage supérieur est composé de matériaux issus de la démolition avec de très nombreuses tuiles, des blocs de schiste brut ainsi que quelques tessons de céramique gallo-romaine. 
    De nombreux trous de poteaux et fosses se situent entre ces deux structures majeures. 
    Un angle de fossé dessinant l’amorce d’un enclos se développe au sud. Du mobilier La Tène finale a également été trouvé dans une fosse située dans cette espace. Un réseau fossoyé se développe à l’est, très érodé du côté nord. 
    Des fragments de céramique possiblement haut Moyen Âge ont été trouvés dans son comblement.'''

    # English example test text from https://doi.org/10.5284/1100093
    pipeline = "fr_core_news_sm"
    periodo_authority_id = "p0kh9ds"
    test_text = """This collection comprises site data(reports, images, spreadsheets, GIS data and site records) from two phases of archaeological evaluation undertaken by Oxford Archaeology in June 2018 (SAWR18) and February 2021 (SAWR21) at West Road, Sawbridgeworth, Hertfordshire. SAWR18 In June 2018, Oxford Archaeology were commissioned by Taylor Wimpey to undertake an archaeological evaluation on the site of a proposed housing development to the north of West Road, Sawbridgeworth(TL 47842 15448). A programme of 19 trenches was undertaken to ground truth the results of a geophysical survey and to assess the archaeological potential of the site. The evaluation confirmed the presence of archaeological remains in areas identified on the geophysics. Parts of a NW-SE‐aligned trackway were found in Trenches 1 and 2. Field boundaries identified by geophysics(also present on the 1839 tithe map) were found in Trenches 5 and 7, towards the south of the site, and in Trenches 12 and 16, in the centre of the site. Geophysical anomalies identified in the northern part of the site were investigated and identified as geological. The archaeology is consistent with the geophysical survey results and it is likely that much of it has been truncated by modern agricultural activity. SAWR21 Oxford Archaeology carried out an archaeological evaluation on the site of proposed residential development north of West Road, Sawbridgeworth, Hertfordshire, in February 2021. The fieldwork was commissioned by Taylor Wimpey as a condition of planning permission. Preceding geophysical survey of the c 5.7ha development site was undertaken in 2016 and identified a concentration of linear and curvilinear anomalies in the north-east corner of the site and two areas of several broadly NW-SE aligned anomalies in the southern half of the site. Subsequent trial trench evaluation, comprising the investigation of 19 trenches, was undertaken by Oxford Archaeology in 2018, targeted upon the geophysical survey results. The evaluation revealed a small number of ditches in the centre and south of the site, correlating with the geophysical anomalies. Although generally undated, the ditches were suggestive of a trackway and associated enclosure/field boundaries. Other ditches encountered on site correlated with post-medieval field boundaries depicted on 19th century mapping. Given the results of the 2018 evaluation, in conjunction with those of the 2018 investigations at nearby Chalk's Farm, which uncovered the remains of Late Bronze Age-early Iron Age and early Roman settlement and agricultural activity, it was deemed necessary to undertake a further phase of evaluation at the site. Four additional trenches were excavated in the southern half of the site to further investigate the previously revealed ditches. The continuations of the trackway ditches were revealed in the centre of the site, with remnants of a metalled surface also identified. Adjacent ditches may demonstrate the maintenance and modification of the trackway or perhaps associated enclosure/field boundaries. Artefactual dating evidence recovered from these ditches was limited and of mixed date, comprising small pottery sherds of late Bronze Age- Early Iron Age date and fragments of Roman ceramic building material. It is probable that these remains provide evidence of outlying agricultural activity associated with the later prehistoric and early Roman settlement evidence at Chalk's Farm. A further undated ditch and a parallel early Roman ditch were revealed in the south of the site, suggestive of additional land divisions, probably agricultural features. A post-medieval field boundary ditch and modern land drains are demonstrative of agricultural use of the landscape during these periods."""
    nlp = get_pipeline_for_language("fr")
    # nlp.max_length = 2000000

    nlp.add_pipe("periodo_ruler", last=True, config={
                 "periodo_authority_id": periodo_authority_id})
    doc = nlp(test_text)
    
    print("Tokens:\n" + DocSummary(doc).tokens("text"))
    print("Spans:\n")
    print([(span.text, span.label_) for span in doc.spans["custom"]])
    