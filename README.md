# Information Extraction Components

- [Introduction](#introduction)
  - [Supported languages](#languages)
  - [Patterns](#patterns)
- [Components](#components)
  - [dayname_ruler](#dayname_ruler)
  - [monthname_ruler](#monthname_ruler)
  - [seasonname_ruler](#seasonname_ruler)
  - [ordinal_ruler](#ordinal_ruler)
  - [dateprefix_ruler](#dateprefix_ruler)
  - [datesuffix_ruler](#datesuffix_ruler)
  - [yearspan_ruler](#yearspan_ruler)
  - [periodo_ruler](#periodo_ruler)
  - [vocabulary_ruler](#vocabulary_ruler)
  - [geonames_ruler](#geonames_ruler)  
- [Usage](#usage)
  - [temporal component usage](#temporal_usage)
  - [vocabulary component usage](#vocabulary_usage)
  - [geographical component usage](#geographical_usage)


## Introduction <a class="anchor" id="introduction"></a>

`rematch2` is an open-source set of components for use with the [spaCy](https://spacy.io) library for performing multilingual rule-based information extraction on abstracts and texts relating to archaeological investigations. The components were originally created by [University of South Wales](https://www.southwales.ac.uk/research/research-and-innovation-groups/computing-cybersecurity-mathematics-and-informatics/) as part of the [ARIADNEplus project](https://ariadne-infrastructure.eu/), and subsequently significantly improved and extended as part of the [ATRIUM project](https://atrium-research.eu/).

### Supported languages <a class="anchor" id="languages"></a>

The languages currently supported by the `rematch2` pipeline temporal components are:

- German (de)
- English (en)
- Spanish (es)
- French (fr)
- Italian (it)
- Dutch (nl)
- Norwegian (no)
- Swedish (sv)

For the vocabulary-driven pipeline component the supported language is the language of the given vocabulary. The examples we give are expressed in English.

### Patterns <a class="anchor" id="patterns"></a>

The pipeline components utilise predefined spaCy _patterns_ which are located in the _spacypatterns_ directory. These are python modules using the naming convention `patterns_{language}_{ENTITYTYPE}.py` e.g. `patterns_en_YEARSPAN.py`. For further details on the required syntax of patterns see [spaCy rule-based matching](https://spacy.io/usage/rule-based-matching).

## Components <a class="anchor" id="components"></a>

`rematch2` performs specialised information extraction on temporal, geographical and vocabulary entities, and implements specialised spaCy pipeline components to identify the following entity types in free text. Note the actual 'Entity Type' can be configured to suit when using the pipeline component:

| Component Name                        | Entity Type | Description                                                            |                                             Examples |
| ------------------------------------- | ----------- | ---------------------------------------------------------------------- | ---------------------------------------------------: |
| [dayname_ruler](#dayname_ruler)       | DAYNAME     | Day names and their common abbreviations                               |                              _Mon., TUES, Wednesday_ |
| [monthname_ruler](#monthname_ruler)   | MONTHNAME   | Month names and their common abbreviations                             |                                   _Jan., FEB, March_ |
| [seasonname_ruler](#seasonname_ruler) | SEASONNAME  | Season names                                                           |               _Spring, SUMMER, Autumn, WINTER, Fall_ |
| [ordinal_ruler](#ordinal_ruler)       | ORDINAL     | Expressions of ordinals (used in identifying centuries)                |                             _1st, first, THIRD, 3RD_ |
| [dateprefix_ruler](#dateprefix_ruler) | DATEPREFIX  | Prefixes commonly associated with years, spans and centuries           |    _Circa, Early, earlier, mid, MIDDLE, Late, later_ |
| [datesuffix_ruler](#datesuffix_ruler) | DATESUFFIX  | Prefixes commonly associated with years, spans and centuries           |                       _A.D., AD, B.C., BC, B.P., BP_ |
| [yearspan_ruler](#yearspan_ruler)     | YEARSPAN    | Spans of years or centuries (possibly with prefixes and/or suffixes)   |                         _early 1300 to late 1350 AD_ |
| [periodo_ruler](#periodo_ruler)       | PERIOD      | Period label from specified [Perio.do](https://perio.do/en/) authority |              _Bronze Age, Early Medieval, Victorian_ |
| [vocabulary_ruler](#vocabulary_ruler) | (user specified) | Labels from supplied controlled vocabulary of terms              |      _Brooch, Mineralogy, Leather, Cropmark, Hearth_ |
| [geonames_ruler](#geonames_ruler)     | PLACE       | Place names from the [GeoNames](https://www.geonames.org/) dataset     |              _Oxford, Sawbridgeworth, Hertfordshire_ |

### dayname_ruler <a class="anchor" id="dayname_ruler"></a>

Identifies day names or their abbreviations in text. Not currently used, but remains present as a concrete example showing how to implement a custom multilingual pattern-based ruler.

### monthname_ruler <a class="anchor" id="monthname_ruler"></a>

Identifies month names or their abbreviations in text. Used by the _yearspan_ruler_ to identify pattern of month followed by year e.g. _June 1867_

### seasonname_ruler <a class="anchor" id="seasonname_ruler"></a>

Identifies season names in text. Used by the _yearspan_ruler_ to identify pattern of season followed by year e.g. _Spring 1867_

### ordinal_ruler <a class="anchor" id="ordinal_ruler"></a>

Identifies ordinal expressions in text e.g. _15th, nineteenth_. Used by the _yearspan_ruler_ to identify pattern of ordinal followed by century e.g. _15th century_, _nineteenth century_. As an alternative spaCy does have its own built in NER functionality which includes identification of ordinals; these patterns were developed prior to adopting spaCy.

### dateprefix_ruler <a class="anchor" id="dateprefix_ruler"></a>

Identifies typical dating prefixes in text. Used by the _yearspan_ruler_ to identify patterns of prefixes followed by century or year e.g. _early 1867_, _circa mid 19th century_

### datesuffix_ruler <a class="anchor" id="datesuffix_ruler"></a>

Identifies typical dating suffixes in text. Used by the _yearspan_ruler_ to identify patterns of year or century followed by suffix e.g. _early 1867 AD_, _5th century BC_

### yearspan_ruler <a class="anchor" id="yearspan_ruler"></a>

Identifies typical expressions of years or spans of years in text. Utilises other rulers to identify more complex patterns e.g. _late 1712 to early 1714 AD_

### periodo_ruler <a class="anchor" id="periodo_ruler"></a>

The periodo ruler component utilises the [Perio.do](https://perio.do/) dataset. When configured with a valid Perio.do authority identifier e.g. `'p0xxt6t'` [Scottish Archaeological Periods & Ages (ScAPA)](http://n2t.net/ark:/99152/p0xxt6t), the component will match against the labels of periods contained within that specified authority. e.g. _Chalcolithic, Early Bronze Age, Antonine_

### vocabulary_ruler <a class="anchor" id="vocabulary_ruler"></a>
Example vocabulary files are included for use with the vocabulary_ruler component to identify terms originating from extracts of controlled vocabularies as occurring in free text. The (suggested) 'Entity Type' given below can be overriden when configuring the pipeline. Sometimes a vocabulary may not quite fit the use case of terms to be located - controlled vocabularies do not always contain the exact terms as used in free-text. In this case there is the flexibility of directly editing the pattern file used, and/or including an additional supplementary file (e.g. to expand the entry vocabulary), and/or a 'stop file' containing identifiers that should NOT appear in the results. 

The example files described in the table below contain terms and Linked Open Data (LOD) identifiers extracted from the [Getty Art &amp; Architecture Thesaurus (AAT)](https://www.getty.edu/research/tools/vocabularies/aat/) SPARQL endpoint, and from the [FISH 'Heritage Standards'](https://heritage-standards.org.uk/fish-vocabularies/) site for bulk downloads of vocabulary data. Note the file naming convention indicates the date the data was extracted and the file created - so they are a snapshot and do not represent the latest version of the controlled vocabularies. The user is directed to the originating sites for the most up to date information.

| Vocabulary File                                | Source Description                                                                   | Examples                                                           |
| ---------------------------------------------- | ------------------------------------------------------------------------------------ | -----------------------------------------------------------------: |
| patterns_AAT_ACTIVITIES_YYYYMMDD.json          | [Getty AAT 'Activities' facet](http://vocab.getty.edu/aat/300264090)                 | [vibrational spectroscopy](http://vocab.getty.edu/aat/300390577)   |
| patterns_AAT_AGENTS_YYYYMMDD.json              | [Getty AAT 'Agents' facet](http://vocab.getty.edu/aat/300264089)                     | [archaeologists](http://vocab.getty.edu/aat/300025486)             |
| patterns_AAT_ASSOCIATED_CONCEPTS_YYYYMMDD.json | [Getty AAT 'Associated Concepts' facet](http://vocab.getty.edu/aat/300264086)        | [chemiluminescence](http://vocab.getty.edu/aat/300191614)          |
| patterns_AAT_MATERIALS_YYYYMMDD.json           | [Getty AAT 'Materials' facet](http://vocab.getty.edu/aat/300264091)                  | [Aurene glass](http://vocab.getty.edu/aat/300206172)               |
| patterns_AAT_OBJECTS_YYYYMMDD.json             | [Getty AAT 'Objects' facet](http://vocab.getty.edu/aat/300264092)                    | [flintlock musket](http://vocab.getty.edu/aat/300425686)           |
| patterns_AAT_PHYSICAL_ATTRIBUTES_YYYYMMDD.json | [Getty AAT 'Physical Attributes' facet](http://vocab.getty.edu/aat/300264087)        | [compressive strength](http://vocab.getty.edu/aat/300379461)       |
| patterns_AAT_STYLEPERIODS_YYYYMMDD.json        | [Getty AAT 'Styles &amp; Periods' facet](http://vocab.getty.edu/aat/300264088)       | [Cambrian](http://vocab.getty.edu/aat/300391263)                   |
| patterns_FISH_73_YYYYMMDD.json                 | [FISH 'Object Materials' thesaurus](http://purl.org/heritagedata/schemes/73)         | [bronze](http://purl.org/heritagedata/schemes/73/concepts/75344)                  |
| patterns_FISH_560_YYYYMMDD.json                | [FISH 'Archaeological Sciences' thesaurus](http://purl.org/heritagedata/schemes/560) | [biostratigraphy](http://purl.org/heritagedata/schemes/560/concepts/142107)       |
| patterns_FISH_eh_tbm_YYYYMMDD.json             | [FISH 'Building Materials' thesaurus](http://purl.org/heritagedata/schemes/eh_tbm)   | [alabaster](http://purl.org/heritagedata/schemes/eh_tbm/concepts/97704)           |
| patterns_FISH_eh_com_YYYYMMDD.json             | [FISH 'Components' thesaurus](http://purl.org/heritagedata/schemes/eh_com)           | [clasping buttress](http://purl.org/heritagedata/schemes/eh_com/concepts/137560)  |
| patterns_FISH_agl_et_YYYYMMDD.json             | [FISH 'Event Types' thesaurus](http://purl.org/heritagedata/schemes/agl_et)          | [aerial photography](http://purl.org/heritagedata/schemes/agl_et/concepts/145107) |
| patterns_FISH_eh_evd_YYYYMMDD.json             | [FISH 'Evidence' thesaurus](http://purl.org/heritagedata/schemes/eh_evd)             | [parchmark](http://purl.org/heritagedata/schemes/eh_evd/concepts/78253)           |
| patterns_FISH_eh_tmc_YYYYMMDD.json             | [FISH 'Maritime Craft Types' thesaurus](http://purl.org/heritagedata/schemes/eh_tmc) | [barquentine](http://purl.org/heritagedata/schemes/eh_tmc/concepts/100274)        |
| patterns_FISH_eh_tmt2_YYYYMMDD.json            | [FISH 'Monument Types' thesaurus](http://purl.org/heritagedata/schemes/eh_tmt2)      | [necropolis](http://purl.org/heritagedata/schemes/eh_tmt2/concepts/70053)         |
| patterns_FISH_mda_obj_YYYYMMDD.json            | [FISH 'Archaeological Objects' thesaurus](http://purl.org/heritagedata/schemes/mda_obj) | [goblet](http://purl.org/heritagedata/schemes/mda_obj/concepts/96782)          |


### geonames_ruler <a class="anchor" id="geonames_ruler"></a>
The geonames_ruler component performs a lookup on place names originating from the [GeoNames](https://www.geonames.org/) dataset. In order to enable sufficient performance and reduce the potential for ambiguities, the component configuration accepts one or more ISO country codes (e.g. "GB"). 

## Usage <a class="anchor" id="usage"></a>

### Temporal component usage <a class="anchor" id="temporal_usage"></a>
Both the [yearspans_ruler](#yearspans_ruler) and the [periodo_ruler](#periodo_ruler) perform information extraction of temporal entities. Example Python script to perform information extraction on temporal entities using these components:

```python
import spacy
import pandas as pd
from components import YearSpanRuler, ChildSpanRemover, PeriodoRuler

# use a predefined pipeline, disabling the default NER component
nlp = spacy.load("en_core_web_sm", disable=["ner"])

# add configured custom pipeline component(s) to the pipeline
nlp.add_pipe("yearspan_ruler", last=True)
nlp.add_pipe("periodo_ruler", last=True, config={"periodo_authority_id": "p0kh9ds"})
nlp.add_pipe("child_span_remover", last=True)

# process some example text using the configured pipeline
test_text = """Although generally undated, the ditches were suggestive of a trackway and associated enclosure/field boundaries. Other ditches encountered on site correlated with post-medieval field boundaries depicted on 19th century mapping. Given the results of the 2018 evaluation, in conjunction with those of the 2018 investigations at nearby Chalk's Farm, which uncovered the remains of Late Bronze Age-early Iron Age and early Roman settlement and agricultural activity, it was deemed necessary to undertake a further phase of evaluation at the site."""

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

"""results:
start  end    label                                    id            text
   163  176   PERIOD http://n2t.net/ark:/99152/p0kh9dsctsj   post-medieval
   206  218 YEARSPAN                                          19th century
   378  393   PERIOD http://n2t.net/ark:/99152/p0kh9dsqkbq Late Bronze Age
   394  408   PERIOD http://n2t.net/ark:/99152/p0kh9dszskn  early Iron Age
   413  424   PERIOD http://n2t.net/ark:/99152/p0kh9ds7wqn     early Roman
  """
```

### Vocabulary component usage <a class="anchor" id="vocabulary_usage"></a>
The [vocabulary_ruler](#vocabulary_ruler) component is supplied with a user-defined vocabulary of concepts to be locadted in the text. Ypu can also perform lemmatization for more flexible matching, and part(s) of speech to improve precision. Example Python script to perform information extraction using this component:

```python
# Using specialised VocabularyRuler pipeline component
import json, spacy
import pandas as pd
from components import VocabularyRuler

test_text = """
This collection comprises site data (images, a report, a project database and GIS data) from an archaeological excavation undertaken by Cotswold Archaeology between January and February 2020 at Lydney B Phase III, Archers Walk, Lydney, Gloucestershire. An area of 0.6ha was excavated within this phase (Phase III) of a wider development area.
Aside from three residual flints, none closely datable, the earliest remains comprised a small assemblage of Roman pottery and ceramic building material, also residual and most likely derived from a Roman farmstead found immediately to the north within the Phase II excavation area. A single sherd of Anglo-Saxon grass-tempered pottery was also residual.
The earliest features, which accounted for the majority of the remains on site, relate to medieval agricultural activity focused within a large enclosure. There was little to suggest domestic occupation within the site: the pottery assemblage was modest and well abraded, whilst charred plant remains were sparse, and, as with some metallurgical residues, point to waste disposal rather than the locations of processing or consumption. A focus of occupation within the Rodley Manor site, on higher ground 160m to the north-west, seems likely, with the currently site having lain beyond this and providing agricultural facilities, most likely corrals and pens for livestock. Animal bone was absent, but the damp, low-lying ground would have been best suited to cattle. An assemblage of medieval coins recovered from the subsoil during a metal detector survey may represent a dispersed hoard.
"""

# use a predefined spaCy pipeline, disabling the default NER component
nlp = spacy.load("en_core_web_sm", disable=['ner'])

# add configured custom pipeline component(s) to the pipeline
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

"""results:
start end label       id                                                                                text
370   376 FISH_OBJECT http://purl.org/heritagedata/schemes/mda_obj/concepts/97566                     flints
439   449 FISH_OBJECT http://purl.org/heritagedata/schemes/mda_obj/concepts/141192                assemblage
459   466 FISH_OBJECT http://purl.org/heritagedata/schemes/mda_obj/concepts/137051                   pottery
471   496 FISH_OBJECT http://purl.org/heritagedata/schemes/mda_obj/concepts/141190 ceramic building material
636   641 FISH_OBJECT http://purl.org/heritagedata/schemes/mda_obj/concepts/137051                     sherd
672   679 FISH_OBJECT http://purl.org/heritagedata/schemes/mda_obj/concepts/137051                   pottery
923   930 FISH_OBJECT http://purl.org/heritagedata/schemes/mda_obj/concepts/137051                   pottery
931   941 FISH_OBJECT http://purl.org/heritagedata/schemes/mda_obj/concepts/141192                assemblage
986   999 FISH_OBJECT http://purl.org/heritagedata/schemes/mda_obj/concepts/100093             plant remains
1045 1053 FISH_OBJECT http://purl.org/heritagedata/schemes/mda_obj/concepts/142906                  residues
1353 1357 FISH_OBJECT http://purl.org/heritagedata/schemes/mda_obj/concepts/95390                       pens
1373 1384 FISH_OBJECT http://purl.org/heritagedata/schemes/mda_obj/concepts/95074                Animal bone
1470 1480 FISH_OBJECT http://purl.org/heritagedata/schemes/mda_obj/concepts/141192                assemblage
1493 1498 FISH_OBJECT http://purl.org/heritagedata/schemes/mda_obj/concepts/95423                      coins
1583 1588 FISH_OBJECT http://purl.org/heritagedata/schemes/mda_obj/concepts/97498                      hoard
"""
```

### Geographical component usage <a class="anchor" id="geographical_usage"></a>
The [geonames_ruler](#geonames_ruler) component is an experimental addition, configured with a country code both to improve performance and reduce ambiguity. Example Python script to perform information extraction using this component:

```python
import spacy
import pandas as pd
from components import GeoNamesRuler

nlp = spacy.load("en_core_web_sm", disable=["ner"])

# example text
test_text = """This collection comprises Roman site data(reports, images, spreadsheets, GIS data and site records) from two phases of archaeological evaluation undertaken by Oxford Archaeology in June 2018 (SAWR18) and February 2021 (SAWR21) at West Road, Sawbridgeworth, Hertfordshire. SAWR18 In June 2018, Oxford Archaeology were commissioned by Taylor Wimpey to undertake an archaeological evaluation on the site of a proposed housing development to the north of West Road, Sawbridgeworth (TL 47842 15448)."""
nlp.add_pipe("geonames_ruler", last=True, config={"country_codes": ["GB"]})

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

"""results:
start end label                               id           text
159   165 PLACE http://sws.geonames.org/2640729/         Oxford
241   255 PLACE http://sws.geonames.org/2638481/ Sawbridgeworth
257   270 PLACE http://sws.geonames.org/2647043/  Hertfordshire
293   299 PLACE http://sws.geonames.org/2640729/         Oxford
462   476 PLACE http://sws.geonames.org/2638481/ Sawbridgeworth
"""
```

Other practical examples of spaCy pipeline component usage may be found in the accompanying Python notebooks.
