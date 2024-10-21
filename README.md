# rematch2 components

- [Introduction](#introduction)
  - [Supported Languages](#languages)
- [Patterns](#patterns)
- [Components](#components)
  - [Temporal components](#temporal_components)
    - [dayname_ruler](#dayname_ruler)
    - [monthname_ruler](#monthname_ruler)
    - [seasonname_ruler](#seasonname_ruler)
    - [ordinal_ruler](#ordinal_ruler)
    - [dateprefix_ruler](#dateprefix_ruler)
    - [datesuffix_ruler](#datesuffix_ruler)
    - [yearspan_ruler](#yearspan_ruler)
    - [periodo_ruler](#periodo_ruler)
    - [temporal_annotator](#temporal_annotator)
    - [Temporal component usage](#component_usage)
  - [Geographical components](#geographical_components)  
    - [geonames_ruler](#geonames_ruler)
  - [Vocabulary components](#vocabulary_components)
    - [AAT vocabulary components](#aat_vocabulary_components)
      - [aat_activities_ruler](#aat_activities_ruler)
      - [aat_agents_ruler](#aat_agents_ruler)
      - [aat_associated_concepts_ruler](#aat_associated_concepts_ruler)
      - [aat_materials_ruler](#aat_materials_ruler)
      - [aat_objects_ruler](#aat_objects_ruler)
      - [aat_physical_attributes_ruler](#aat_physical_attributes_ruler)
      - [aat_styleperiods_ruler](#aat_styleperiods_ruler)
    - [FISH vocabulary components](#fish_vocabulary_components)
      - [fish_archobjects_ruler](#fish_archobjects_ruler)
      - [fish_archsciences_ruler](#fish_archsciences_ruler)
      - [fish_building_materials_ruler](#fish_building_materials_ruler)
      - [fish_components_ruler](#fish_components_ruler)
      - [fish_event_types_ruler](#fish_event_types_ruler)
      - [fish_evidence_ruler](#fish_evidence_ruler)
      - [fish_maritime_craft_ruler](#fish_maritime_craft_ruler)
      - [fish_monument_types_ruler](#fish_monument_types_ruler)
      - [fish_periods_ruler](#fish_periods_ruler)
    - [vocabulary_annotator](#vocabulary_annotator)
    - [Vocabulary Annotator usage](#vocabulary_annotator_usage)

## Introduction <a class="anchor" id="introduction"></a>

`rematch2` is an experimental [spaCy](https://spacy.io) open-source library and associated tools for performing multilingual rule-based Named Entity Recognition (NER) on abstracts and texts relating to archaeological investigations. The library and tools were created by [University of South Wales Hypermedia Research Group](https://hypermedia.research.southwales.ac.uk/) as part of the [ARIADNEplus project](https://ariadne-infrastructure.eu/), and improved and extended as part of the [ATRIUM project](https://atrium-research.eu/).

### Supported Languages <a class="anchor" id="languages"></a>

The languages (currently) supported by the `rematch2` pipeline temporal components are:

- German
- English
- Spanish
- French
- Italian
- Dutch
- Norwegian
- Swedish

For the vocabulary-driven components the language supported is English - as the vocabularies currently used are expressed in English.

## Patterns <a class="anchor" id="patterns"></a>

The pipeline components utilise spaCy _patterns_ located in the _spacypatterns_ directory, these are python modules using the naming convention `patterns_{language}_{ENTITYTYPE}.py` e.g. `patterns_en_YEARSPAN.py`. For further details on the syntax of patterns see [spaCy rule-based matching](https://spacy.io/usage/rule-based-matching).

## Components <a class="anchor" id="components"></a>

### Temporal Components <a class="anchor" id="temporal_components"></a>

`rematch2` performs specialised NER focussed on temporal entities, and implements specialised spaCy pipeline components to identify the following entity types in free text:

| Component Name                        | Entity Type | Description                                                              |                                             Examples |
| ------------------------------------- | ----------- | ------------------------------------------------------------------------ | ---------------------------------------------------: |
| [dayname_ruler](#dayname_ruler)       | DAYNAME     | Day names and their common abbreviations                                 |                              _Mon., TUES, Wednesday_ |
| [monthname_ruler](#monthname_ruler)   | MONTHNAME   | Month names and their common abbreviations                               |                                   _Jan., FEB, March_ |
| [seasonname_ruler](#seasonname_ruler) | SEASONNAME  | Season names                                                             |               _Spring, SUMMER, Autumn, WINTER, Fall_ |
| [ordinal_ruler](#ordinal_ruler)       | ORDINAL     | Expressions of ordinals (used in identifying centuries)                  |                             _1st, first, THIRD, 3RD_ |
| [dateprefix_ruler](#dateprefix_ruler) | DATEPREFIX  | Prefixes commonly associated with years, spans and centuries             |    _Circa, Early, earlier, mid, MIDDLE, Late, later_ |
| [datesuffix_ruler](#datesuffix_ruler) | DATESUFFIX  | Prefixes commonly associated with years, spans and centuries             |                       _A.D., AD, B.C., BC, B.P., BP_ |
| [yearspan_ruler](#yearspan_ruler)     | YEARSPAN    | Spans of years or centuries (possibly with prefixes and/or suffixes)     |                         _early 1300 to late 1350 AD_ |
| [periodo_ruler](#periodo_ruler)       | PERIOD      | Period label from a specified [Perio.do](https://perio.do/en/) authority |              _Bronze Age, Early Medieval, Victorian_ |

### dayname_ruler <a class="anchor" id="dayname_ruler"></a>

Identifies day names or their abbreviations in text. Not currently used by other rulers, but remains present and usable as a concrete example showing how to implement a custom multilingual pattern-based ruler.

### monthname_ruler <a class="anchor" id="monthname_ruler"></a>

Identifies month names or their abbreviations in text. Used in combination with other rulers to identify pattern of month followed by year e.g. _June 1867_

### seasonname_ruler <a class="anchor" id="seasonname_ruler"></a>

Identifies season names in text. Used in combination with other rulers to identify pattern of season followed by year e.g. _Spring 1867_

### ordinal_ruler <a class="anchor" id="ordinal_ruler"></a>

Identifies ordinal expressions in text e.g. _15th, nineteenth_. Used in combination with other rulers to identify pattern of ordinal followed by century e.g. _15th century_, _nineteenth century_. As an alternative spaCy does have its own built in NER functionality which includes identification of ordinals; these patterns were developed prior to adopting spaCy

### dateprefix_ruler <a class="anchor" id="dateprefix_ruler"></a>

Identifies typical dating prefixes in text. Used in combination with other rulers to identify patterns of prefixes followed by century or year e.g. _early 1867_, _circa mid 19th century_

### datesuffix_ruler <a class="anchor" id="datesuffix_ruler"></a>

Identifies typical dating suffixes in text. Used in combination with other rulers to identify patterns of year or century followed by suffix e.g. _early 1867 AD_, _5th century BC_

### yearspan_ruler <a class="anchor" id="yearspan_ruler"></a>

Identifies typical expressions of years or spans of years in text. Utilises other rulers to identify more complex patterns e.g. _late 1712 to early 1714 AD_

### periodo_ruler <a class="anchor" id="periodo_ruler"></a>

The periodo ruler component utilises the [Perio.do](https://perio.do/) dataset. When configured with a valid Perio.do authority identifier e.g. `'p0xxt6t'` [Scottish Archaeological Periods & Ages (ScAPA)](http://n2t.net/ark:/99152/p0xxt6t), the component will match against the labels of periods contained within the specified authority. e.g. _Chalcolithic, Early Bronze Age, Antonine_

## Usage <a class="anchor" id="temporal_component_usage"></a>

Example Python script to perform NER using a `rematch2` pipeline component:

```python
import spacy
from rematch2 import create_century_ruler

# use a predefined pipeline, disabling the default NER component
nlp = spacy.load("en_core_web_sm", disable=["ner"])
# add required pipeline component(s) to the end of the pipeline
nlp.add_pipe("century_ruler", last=True)
# process some example text using the modified pipeline
doc = nlp("A late twelfth century AD or early 13th century weapon.")
# display the spans located in the text
for span in doc.spans.get("rematch", []):
  print(span.text)

# results:
# late twelfth century AD
# early 13th century
```

## Temporal Annotator <a class="anchor" id="temporal_annotator"></a>

The temporal annotation components described above are used by the TemporalAnnotator class, which facilitates annotation of text using specified combinations of the components. Example Python script to perform NER using the TemporalAnnotator class:

```python
from rematch2.TemporalAnnotator import TemporalAnnotator

# example test input text copied from https://doi.org/10.5284/1100092
test_text = "This collection comprises site data(reports, images, GIS data and a project database) from an archaeological excavation at Lydney B Phase II, Archers Walk, Lydney, Gloucestershire undertaken by Cotswold Archaeology between February and May 2018. An area of 1.47ha was excavated within this part of a wider development area. The earliest remains comprised three broadly datable flints, all found as residual finds. An Early Bronze Age collared urn within a small pit may be the remains of a grave, although no human remains were found. The first evidence for occupation is from the Roman period, with finds spanning the 1st to 3rd centuries AD, with a clear focus within the 2nd to 3rd centuries. Two phases of Roman activity were identified, the first comprising cereal-processing ovens and two crescent-shaped ditches, one associated with metalworking debris. The later phase comprised stone founded buildings associated with wells, enclosures, trackways and a single cremation deposit. These seem to indicate a Romanised farm below the status of a villa. Little animal bone survived, but the enclosures are suggestive of livestock farming. Occupation seems to have ended in the mid 3rd century, although the reasons for this are not apparent. Further use of the site dates to the medieval period, between the late 12th and 15th centuries, when an agricultural building was constructed, probably an outlier of a manorial farm previously excavated to the west."

# required output format options: html|csv|json|dataframe|doc
# 'html' returns inline markup for visualising annotations in context
# 'dataframe' useful for visualising tabular data in python notebook
# 'csv' and 'json' are useful textual interchange formats
# 'doc' returns the spaCy document object for further processing
output_format = "html"  # options: html|csv|json|dataframe|doc

# if not specified, default ISO639-1 two character language code is "en"
# if not specified, default periodo id is "p0kh9ds" (Historic England periods list)
annotator = TemporalAnnotator(language="en", periodo_authority_id="p0kh9ds")

# process example text and display the results in required output format
results = annotator.annotateText(input_text=test_text, format=output_format)
return results
```

Other practical (interactive) examples of usage are found in the accompanying Python notebooks.

## Geographical components <a class="anchor" id="geographical_components"></a>

### GeoNames ruler <a class="anchor" id="geonames_ruler"></a>
The geonames_ruler component performs a lookup on place names originating from the [GeoNames](https://www.geonames.org/) dataset. In order to enable sufficient performance and reduce the potential for ambiguities, the component configuration accepts one or more ISO country codes.

## Vocabulary Components <a class="anchor" id="vocabulary_components"></a>

### Vocabulary Annotator <a class="anchor" id="vocabulary_annotator"></a>

The VocabularyAnnotator class facilitates annotation of text using a specified vocabulary of terms.

### Usage <a class="anchor" id="vocabulary_annotator_usage"></a>

Example Python script to perform NER using the VocabularyAnnotator class:

```python
# simple example using VocabularyAnnotator on a passage of text
from rematch2.VocabularyAnnotator import VocabularyAnnotator

# example test text from https://doi.org/10.5284/1100093
test_text = """This collection comprises site data (images, a report, a project database and GIS data) from an archaeological excavation undertaken by Cotswold Archaeology between January and February 2020 at Lydney B Phase III, Archers Walk, Lydney, Gloucestershire. An area of 0.6ha was excavated within this phase (Phase III) of a wider development area.
Aside from three residual flints, none closely datable, the earliest remains comprised a small assemblage of Roman pottery and ceramic building material, also residual and most likely derived from a Roman farmstead found immediately to the north within the Phase II excavation area. A single sherd of Anglo-Saxon grass-tempered pottery was also residual.
The earliest features, which accounted for the majority of the remains on site, relate to medieval agricultural activity focused within a large enclosure. There was little to suggest domestic occupation within the site: the pottery assemblage was modest and well abraded, whilst charred plant remains were sparse, and, as with some metallurgical residues, point to waste disposal rather than the locations of processing or consumption. A focus of occupation within the Rodley Manor site, on higher ground 160m to the north-west, seems likely, with the currently site having lain beyond this and providing agricultural facilities, most likely corrals and pens for livestock. Animal bone was absent, but the damp, low-lying ground would have been best suited to cattle. An assemblage of medieval coins recovered from the subsoil during a metal detector survey may represent a dispersed hoard.
"""

# required output format options: html|csv|json|dataframe|doc
# 'html' returns inline markup for visualising annotations in context
# 'dataframe' useful for visualising tabular data in python notebook
# 'csv' and 'json' are useful textual interchange formats
# 'doc' returns the spaCy document object for further processing
output_format = "html"

# create and configure the annotator
annotator = VocabularyAnnotator(vocabs=[VocabularyEnum.FISH_MONUMENT_TYPES])

# process example text and display the results in required output format
results = annotator.annotateText(input_text=test_text, output_format=output_format)
return results
```

`rematch2` also implements specialised spaCy pipeline components to identify terms from the following pre-defined vocabularies in free text:

| Component Name                                                  | Entity Type             | Description | Examples |
| --------------------------------------------------------------- | ----------------------- | ----------- | -------: |
| [aat_activities_ruler](#aat_activities_ruler)                   | AAT_ACTIVITY            |             |          |
| [aat_agents_ruler](#aat_agents_ruler)                           | AAT_AGENT               |             |          |
| [aat_associated_concepts_ruler](#aat_associated_concepts_ruler) | AAT_ASSOCIATED_CONCEPT  |             |          |
| [aat_materials_ruler](#aat_materials_ruler)                     | AAT_MATERIAL            |             |          |
| [aat_objects_ruler](#aat_objects_ruler)                         | AAT_OBJECT              |             |          |
| [aat_physical_attributes_ruler](#aat_physical_attributes_ruler) | AAT_PHYSICAL_ATTRIBUTE  |             |          |
| [aat_styleperiods_ruler](#aat_styleperiods_ruler)               | AAT_STYLEPERIOD         |             |          |
| [fish_archobjects_ruler](#fish_archobjects_ruler)               | AAT_OBJECT              |             |          |
| [fish_archsciences_ruler](#fish_archsciences_ruler)             | FISH_ARCHSCIENCE        |             |          |
| [fish_building_materials_ruler](#fish_building_materials_ruler) | FISH_MATERIAL           |             |          |
| [fish_components_ruler](#fish_components_ruler)                 | FISH_OBJECT             |             |          |
| [fish_event_types_ruler](#fish_event_types_ruler)               | FISH_EVENT              |             |          |
| [fish_evidence_ruler](#fish_evidence_ruler)                     | FISH_ARCHSCIENCE        |             |          |
| [fish_maritime_craft_ruler](#fish_maritime_craft_ruler)         | FISH_OBJECT             |             |          |
| [fish_monument_types_ruler](#fish_monument_types_ruler)         | FISH_OBJECT             |             |          |
| [fish_periods_ruler](#fish_periods_ruler)                       | FISH_PERIOD             |             |          |
| [geonames_ruler](#geonames_ruler)                               | PLACE                   |             |          |

## Getty Art &amp; Architecture Thesaurus (AAT) vocabulary components <a class="anchor" id="aat_vocabulary_components"></a>

Components to identify terms originating from the [Getty Art &amp; Architecture Thesaurus (AAT)](https://www.getty.edu/research/tools/vocabularies/aat/)

### aat_activities_ruler <a class="anchor" id="aat_activities_ruler"></a>

Identifies terms from the [AAT 'Activities' facet](http://vocab.getty.edu/aat/300264090)

### aat_agents_ruler <a class="anchor" id="aat_agents_ruler"></a>

Identifies terms from the [AAT 'Agents' facet](http://vocab.getty.edu/aat/300264089)

### aat_associated_concepts_ruler <a class="anchor" id="aat_associated_concepts_ruler"></a>

Identifies terms from the [AAT 'Associated Concepts' facet](http://vocab.getty.edu/aat/300264086)

### aat_materials_ruler <a class="anchor" id="aat_materials_ruler"></a>

Identifies terms from the [AAT 'Materials' facet](http://vocab.getty.edu/aat/300264091)

### aat_objects_ruler <a class="anchor" id="aat_objects_ruler"></a>

Identifies terms from the [AAT 'Objects' facet](http://vocab.getty.edu/aat/300264092)

### aat_physical_attributes_ruler <a class="anchor" id="aat_physical_attributes_ruler"></a>

Identifies terms from the [AAT 'Physical Attributes' facet](http://vocab.getty.edu/aat/300264087)

### aat_styleperiods_ruler <a class="anchor" id="aat_styleperiods_ruler"></a>

Identifies terms from the [AAT 'Styles &amp; Periods' facet](http://vocab.getty.edu/aat/300264088)

## Forum on Information Standards in Heritage (FISH) vocabulary components <a class="anchor" id="fish_vocabulary_components"></a>

Components to identify terms originating from [Forum on Information Standards in Heritage](https://www.heritage-standards.org.uk/) (FISH) vocabularies

### fish_archobjects_ruler <a class="anchor" id="fish_archobjects_ruler"></a>

Identifies terms from the [FISH 'Archaeological Objects' thesaurus](http://purl.org/heritagedata/schemes/mda_obj)

### fish_archsciences_ruler <a class="anchor" id="fish_archsciences_ruler"></a>

Identifies terms from the [FISH 'Archaeological Sciences' thesaurus](http://purl.org/heritagedata/schemes/560)

### fish_building_materials_ruler <a class="anchor" id="fish_building-materials_ruler"></a>

Identifies terms from the [FISH 'Building Materials' thesaurus](http://purl.org/heritagedata/schemes/eh_tbm)

### fish_components_ruler <a class="anchor" id="fish_components_ruler"></a>

Identifies terms from the [FISH 'Components' thesaurus](http://purl.org/heritagedata/schemes/eh_com)

### fish_event_types_ruler <a class="anchor" id="fish_event_types_ruler"></a>

Identifies terms from the [FISH 'Event Types' thesaurus](http://purl.org/heritagedata/schemes/agl_et)

### fish_evidence_ruler <a class="anchor" id="fish_evidence_ruler"></a>

Identifies terms from the [FISH 'Evidence' thesaurus](http://purl.org/heritagedata/schemes/eh_evd)

### fish_maritime_craft_ruler <a class="anchor" id="fish_maritime_craft_ruler"></a>

Identifies terms from the [FISH 'Maritime Craft Types' thesaurus](http://purl.org/heritagedata/schemes/eh_tmc)

### fish_monument_types_ruler <a class="anchor" id="fish_monument_types_ruler"></a>

Identifies terms from the [FISH 'Monument Types' thesaurus](http://purl.org/heritagedata/schemes/eh_tmt2)

### fish_periods_ruler <a class="anchor" id="fish_periods_ruler"></a>

Identifies terms from the [FISH 'Historic England Periods' thesaurus](http://purl.org/heritagedata/schemes/eh_period)

## Usage <a class="anchor" id="component_usage"></a>

Example Python script to perform NER using the components:

```python
# Using specialised VocabularyRuler pipeline components
import spacy
from spacy import displacy
from rematch2.VocabularyRuler import *

test_text = """
This collection comprises site data (images, a report, a project database and GIS data) from an archaeological excavation undertaken by Cotswold Archaeology between January and February 2020 at Lydney B Phase III, Archers Walk, Lydney, Gloucestershire. An area of 0.6ha was excavated within this phase (Phase III) of a wider development area.
Aside from three residual flints, none closely datable, the earliest remains comprised a small assemblage of Roman pottery and ceramic building material, also residual and most likely derived from a Roman farmstead found immediately to the north within the Phase II excavation area. A single sherd of Anglo-Saxon grass-tempered pottery was also residual.
The earliest features, which accounted for the majority of the remains on site, relate to medieval agricultural activity focused within a large enclosure. There was little to suggest domestic occupation within the site: the pottery assemblage was modest and well abraded, whilst charred plant remains were sparse, and, as with some metallurgical residues, point to waste disposal rather than the locations of processing or consumption. A focus of occupation within the Rodley Manor site, on higher ground 160m to the north-west, seems likely, with the currently site having lain beyond this and providing agricultural facilities, most likely corrals and pens for livestock. Animal bone was absent, but the damp, low-lying ground would have been best suited to cattle. An assemblage of medieval coins recovered from the subsoil during a metal detector survey may represent a dispersed hoard.
"""

# create pipeline and add one or more custom pipeline components
nlp = spacy.load("en_core_web_sm", disable=['ner'])
# AAT vocabulary pipeline components
nlp.add_pipe("aat_activities_ruler", last=True)
# nlp.add_pipe("aat_agents_ruler", last=True)
# nlp.add_pipe("aat_associated_concepts_ruler", last=True)
# nlp.add_pipe("aat_materials_ruler", last=True)
# nlp.add_pipe("aat_objects_ruler", last=True)
# nlp.add_pipe("aat_physical_attributes_ruler", last=True)
# nlp.add_pipe("aat_styleperiods_ruler", last=True)
# FISH vocabulary pipeline components
# nlp.add_pipe("fish_archobjects_ruler", last=True)
# nlp.add_pipe("fish_archsciences_ruler", last=True)
# nlp.add_pipe("fish_building_materials_ruler", last=True)
# nlp.add_pipe("fish_components_ruler", last=True)
# nlp.add_pipe("fish_event_types_ruler", last=True)
# nlp.add_pipe("fish_evidence_ruler", last=True)
# nlp.add_pipe("fish_maritime_craft_ruler", last=True)
nlp.add_pipe("fish_monument_types_ruler", last=True)
# nlp.add_pipe("fish_periods_ruler", last=True)

doc = nlp(test_text)
spans = doc.spans.get("rematch", [])

# create DataFrame with required columns
df = pd.DataFrame([{
  "start": span.start_char,
  "end": span.end_char,
  "token_start": span.start,
  "token_end": span.end - 1,            
  "label": span.label_,
  "id": span.id_,
  "text": span.text
  } for span in spans])

print(df)
```

Other practical examples of usage are found in the accompanying Python notebooks.
