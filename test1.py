# Using specialised VocabularyRuler pipeline component
import json, spacy
import pandas as pd
from components import VocabularyRuler

test_text = """
This collection comprises site data (images, a report, a project database and GIS data) from an archaeological excavation undertaken by Cotswold Archaeology between January and February 2020 at Lydney B Phase III, Archers Walk, Lydney, Gloucestershire. An area of 0.6ha was excavated within this phase (Phase III) of a wider development area.
Aside from three residual flints, none closely datable, the earliest remains comprised a small assemblage of Roman pottery and ceramic building material, also residual and most likely derived from a Roman farmstead found immediately to the north within the Phase II excavation area. A single sherd of Anglo-Saxon grass-tempered pottery was also residual.
The earliest features, which accounted for the majority of the remains on site, relate to medieval agricultural activity focused within a large enclosure. There was little to suggest domestic occupation within the site: the pottery assemblage was modest and well abraded, whilst charred plant remains were sparse, and, as with some metallurgical residues, point to waste disposal rather than the locations of processing or consumption. A focus of occupation within the Rodley Manor site, on higher ground 160m to the north-west, seems likely, with the currently site having lain beyond this and providing agricultural facilities, most likely corrals and pens for livestock. Animal bone was absent, but the damp, low-lying ground would have been best suited to cattle. An assemblage of medieval coins recovered from the subsoil during a metal detector survey may represent a dispersed hoard.
"""

# create spaCy pipeline and add custom pipeline component(s)
nlp = spacy.load("en_core_web_sm", disable=['ner'])

nlp.add_pipe(
  "vocabulary_ruler", 
  name = "object_types_ruler",          # unique name for pipeline component
  last = True,                          # add component at end of pipeline
  config = {
    "default_label": "FISH_OBJECT",     # label to apply to located spans
    "token_pos": ["NOUN"],              # part of speech to match on term    
    "lemmatize": True,                  # lemmatize terms for better matching
    "min_lemm_length": 3,               # min length of term to be lemmatized
    "min_term_length": 3,               # min length of term to be included
    "patt_list": json.load(open("./vocabularies/patterns_FISH_mda_obj_20260513.json"))
  }) 

# run the pipeline on test text
doc = nlp(test_text)
spans = doc.spans.get("rematch", [])

# create DataFrame with required columns
df = pd.DataFrame([{
  "start": span.start_char,
  "end": span.end_char,
  "label": span.label_,
  "id": span.id_,
  "text": span.text
  } for span in spans])

# output results
print(df.to_string(index=False))

'''results
start  end     label                                                            id                      text
370  376 FISH_OBJECT   http://purl.org/heritagedata/schemes/mda_obj/concepts/97566                    flints
439  449 FISH_OBJECT  http://purl.org/heritagedata/schemes/mda_obj/concepts/141192                assemblage
459  466 FISH_OBJECT  http://purl.org/heritagedata/schemes/mda_obj/concepts/137051                   pottery
471  496 FISH_OBJECT  http://purl.org/heritagedata/schemes/mda_obj/concepts/141190 ceramic building material
636  641 FISH_OBJECT  http://purl.org/heritagedata/schemes/mda_obj/concepts/137051                     sherd
672  679 FISH_OBJECT  http://purl.org/heritagedata/schemes/mda_obj/concepts/137051                   pottery
923  930 FISH_OBJECT  http://purl.org/heritagedata/schemes/mda_obj/concepts/137051                   pottery
931  941 FISH_OBJECT  http://purl.org/heritagedata/schemes/mda_obj/concepts/141192                assemblage
986  999 FISH_OBJECT  http://purl.org/heritagedata/schemes/mda_obj/concepts/100093             plant remains
1045 1053 FISH_OBJECT http://purl.org/heritagedata/schemes/mda_obj/concepts/142906                  residues
1353 1357 FISH_OBJECT  http://purl.org/heritagedata/schemes/mda_obj/concepts/95390                      pens
1373 1384 FISH_OBJECT  http://purl.org/heritagedata/schemes/mda_obj/concepts/95074               Animal bone
1470 1480 FISH_OBJECT http://purl.org/heritagedata/schemes/mda_obj/concepts/141192                assemblage
1493 1498 FISH_OBJECT  http://purl.org/heritagedata/schemes/mda_obj/concepts/95423                     coins
1583 1588 FISH_OBJECT  http://purl.org/heritagedata/schemes/mda_obj/concepts/97498                     hoard
'''