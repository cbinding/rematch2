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
    - [century_ruler](#century_ruler)
    - [yearspan_ruler](#yearspan_ruler)
    - [namedperiod_ruler](#namedperiod_ruler)
    - [temporal_annotator](#temporal_annotator)  
  - [Usage](#component_usage)
  - [Vocabulary-based components](#vocabulary_components)
    - [archscience_ruler](#archscience_ruler)
    - [material_ruler](#material_ruler)
    - [monument_ruler](#monument_ruler)
    - [vocabulary_annotator](#vocabulary_annotator)  

## Introduction <a class="anchor" id="introduction"></a>

`rematch2` is an experimental [spaCy](https://spacy.io) open-source library and associated tools for performing multilingual rule-based Named Entity Recognition (NER) on abstracts and texts relating to archaeological investigations. The library and tools were created by [University of South Wales Hypermedia Research Group](https://hypermedia.research.southwales.ac.uk/) as part of the [ARIADNEplus project](https://ariadne-infrastructure.eu/).

### Supported Languages <a class="anchor" id="languages"></a>

The languages (currently) supported by the `rematch2` pipeline components are:

- German
- English
- Spanish
- French
- Italian
- Dutch
- Norwegian
- Swedish

## Patterns <a class="anchor" id="patterns"></a>

The pipeline components are located in the _components_ directory. The components utilise spaCy _patterns_ located in the _patterns_ directory, these are python modules using the naming convention `patterns_{language}_{ENTITYTYPE}.py` e.g. `patterns_en_YEARSPAN.py`. For further details on the syntax of patterns see [spaCy rule-based matching](https://spacy.io/usage/rule-based-matching).

## Components <a class="anchor" id="components"></a>

### Temporal Components <a class="anchor" id="temporal_components"></a>

`rematch2` performs specialised NER focussed on temporal entities, and implements specialised spaCy pipeline components to identify the following entity types in free text:

| Component Name                          | Entity Type | Description                                                              |                                             Examples |
| --------------------------------------- | ----------- | ------------------------------------------------------------------------ | ---------------------------------------------------: |
| [dayname_ruler](#dayname_ruler)         | DAYNAME     | Day names and their common abbreviations                                 |                              _Mon., TUES, Wednesday_ |
| [monthname_ruler](#monthname_ruler)     | MONTHNAME   | Month names and their common abbreviations                               |                                   _Jan., FEB, March_ |
| [seasonname_ruler](#seasonname_ruler)   | SEASONNAME  | Season names                                                             |               _Spring, SUMMER, Autumn, WINTER, Fall_ |
| [ordinal_ruler](#ordinal_ruler)         | ORDINAL     | Expressions of ordinals (used in identifying centuries)                  |                             _1st, first, THIRD, 3RD_ |
| [dateprefix_ruler](#dateprefix_ruler)   | DATEPREFIX  | Prefixes commonly associated with years, spans and centuries             |    _Circa, Early, earlier, mid, MIDDLE, Late, later_ |
| [datesuffix_ruler](#datesuffix_ruler)   | DATESUFFIX  | Prefixes commonly associated with years, spans and centuries             |                       _A.D., AD, B.C., BC, B.P., BP_ |
| [century_ruler](#century_ruler)         | CENTURY     | Ordinal century expression                                               | _early 15th century BC to late fifteenth century AD_ |
| [yearspan_ruler](#yearspan_ruler)       | YEARSPAN    | Spans of years (possibly with prefixes and/or suffixes)                  |                         _early 1300 to late 1350 AD_ |
| [namedperiod_ruler](#namedperiod_ruler) | NAMEDPERIOD | Period label from a specified [Perio.do](https://perio.do/en/) authority |              _Bronze Age, Early Medieval, Victorian_ |

### dayname_ruler <a class="anchor" id="dayname_ruler"></a>

Identifies day names or their abbreviations in text. Not currently used by other rulers, but remains present and usable as a concrete example showing how to implement a custom multilingual entity recognition pattern ruler.

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

### century_ruler <a class="anchor" id="century_ruler"></a>

Identifies typical expressions of centuries or spans of centuries in text. Utilises other rulers to identify more complex patterns e.g. _circa early 5th to late fourth century BC_

### yearspan_ruler <a class="anchor" id="yearspan_ruler"></a>

Identifies typical expressions of years or spans of years in text. Utilises other rulers to identify more complex patterns e.g. _late 1712 to early 1714 AD_

### namedperiod_ruler <a class="anchor" id="namedperiod_ruler"></a>

The namedperiod*ruler component utilises the [Perio.do](https://perio.do/) dataset. When configured with a valid Perio.do authority identifier e.g. `'p0xxt6t'` [Scottish Archaeological Periods & Ages (ScAPA)](http://n2t.net/ark:/99152/p0xxt6t), the component will match against the labels of periods contained within the specified authority. e.g. \_Chalcolithic*, _Early Bronze Age_, _Antonine_

## Usage <a class="anchor" id="component_usage"></a>

Example Python script to perform NER using a `rematch2` pipeline component:

```python
import spacy
import rematch2.components

# use a predefined pipeline, disabling the default NER component
nlp = spacy.load("en_core_web_sm", disable=["ner"])
# add required pipeline component(s) to the end of the pipeline
nlp.add_pipe("century_ruler", last=True)
# process some example text using the modified pipeline
doc = nlp("A late twelfth century AD or early 13th century weapon.")
# display the entities located in the text
for ent in doc.ents:
  print(ent.text)

# results:
# late twelfth century AD
# early 13th century
```

## Temporal Annotator <a class="anchor" id="temporal_annotator"></a>

The temporal annotation components are pulled together by the TemporalAnnotator class, which facilitates annotation of text using specified combinations of the components.
Example Python script to perform NER using the TemporalAnnotator class:

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

### Vocabulary-based Components <a class="anchor" id="vocabulary_components"></a>

In addition to temporal entities, `rematch2` also contains vocabulary-based pipeline components for matching on archaeological vocabulary terms. Note these pipeline components are based on monolingual (English) thesauri so they can only (currently) be used to identify English language terms:

| Component Name | Entity Type | Description | Examples  |
| -------------- | ----------- | ----------- | --------: |
| [namedperiod_ruler](#namedperiod_ruler) | NAMEDPERIOD | Terms from Perio.do [Historic England Periods Authority File](http://n2t.net/ark:/99152/p0kh9ds) | _Medieval, Bronze Age_ |
| [archobject_ruler](#archobject_ruler) | OBJECT | Terms from the [FISH Archaeological Objects Thesaurus](http://purl.org/heritagedata/schemes/mda_obj) | _axe, sherds, ring_ |
| [archscience_ruler](#archscience_ruler) | ARCHSCIENCE | Terms from the [FISH Archaeological Sciences Thesaurus](http://purl.org/heritagedata/schemes/560) | _lead isotope dating, palynology_ |
| [component_ruler](#component_ruler) | COMPONENT | Terms from the [HE Components Thesaurus](http://purl.org/heritagedata/schemes/eh_com) | _rafter, truss, flue_ |
| [evidence_ruler](#evidence_ruler) | EVIDENCE | Terms from the [HE Evidence Thesaurus](http://purl.org/heritagedata/schemes/eh_evd) | _cropmark, artefact scatter_ |
| [eventtype_ruler](#eventtype_ruler) | EVENTTYPE | Terms from the [FISH Event Types Thesaurus](http://purl.org/heritagedata/schemes/agl_et) | _core sampling, geophysical survey, evaluation_ |
| [material_ruler](#material_ruler) | MATERIAL | Terms from the [FISH Building Materials Thesaurus](http://purl.org/heritagedata/schemes/eh_tbm) | _brass, quartz, pine, bone, leather_ |
| [maritime_ruler](#maritime_ruler) | MARITIME | Terms from the [FISH Maritime Craft Types Thesaurus](http://purl.org/heritagedata/schemes/eh_tmc) | _galley, salvage tug, dredger_ |
| [monument_ruler](#monument_ruler) | MONUMENT | Terms from the [FISH Thesaurus of Monument Types](http://purl.org/heritagedata/schemes/eh_tmt2) | _midden, weighbridge, kiln_ |

### archobject_ruler <a class="anchor" id="archobject_ruler"></a>

Identifies types of archaeological objects (i.e. finds) in text

### archscience_ruler <a class="anchor" id="archscience_ruler"></a>

Identifies archaeological science terms in free text

### component_ruler <a class="anchor" id="component_ruler"></a>

Identifies building component terms in free text

### evidence_ruler <a class="anchor" id="evidence_ruler"></a>

Identifies evidence terms in free text

### eventtype_ruler <a class="anchor" id="eventtype_ruler"></a>

Identifies archaeological event type terms in free text

### material_ruler <a class="anchor" id="material_ruler"></a>

Identifies building material terms in free text

### maritime_ruler <a class="anchor" id="maritime_ruler"></a>

Identifies maritime craft type terms in free text

### monument_ruler <a class="anchor" id="monument_ruler"></a>

Identifies monument type terms in free text

## Vocabulary Annotator <a class="anchor" id="vocabulary_annotator"></a>

The vocabulary-based annotation components are pulled together by the VocabularyAnnotator class, which facilitates annotation of text using specified combinations of the components.
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

# entity types may be selectively included/excluded and reordered
# e.g. ["OBJECT", "MONUMENT", "MATERIAL"]
annotator = VocabularyAnnotator(entity_types=[
    "MONUMENT", "EVIDENCE", "MATERIAL",
    "MARITIME", "EVENTTYPE", "ARCHSCIENCE",
    "OBJECT", "COMPONENT", "NAMEDPERIOD"
])

# process example text and display the results in required output format
results = annotator.annotateText(input_text=test_text, format=output_format)
return results
```

Other practical (interactive) examples of usage are found in the accompanying Python notebooks.
