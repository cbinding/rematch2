# rematch2 components

* [Introduction](#introduction)
    * [Supported Languages](#languages)
* [Patterns](#patterns)
* [Components](#components)
    * [Temporal components](#temporal_components)
      * [dayname_ruler](#dayname_ruler)
      * [monthname_ruler](#monthname_ruler)
      * [seasonname_ruler](#seasonname_ruler)
      * [ordinal_ruler](#ordinal_ruler)        
      * [dateprefix_ruler](#dateprefix_ruler)
      * [datesuffix_ruler](#datesuffix_ruler)
      * [century_ruler](#century_ruler)
      * [yearspan_ruler](#yearspan_ruler)
      * [namedperiod_ruler](#namedperiod_ruler)
    * [Supplementary components](#supplementary_components)
      * [archscience_ruler](#archscience_ruler)
      * [material_ruler](#material_ruler)
      * [monument_ruler](#monument_ruler)
  * [Usage](#component_usage)

## Introduction <a class="anchor" id="introduction"></a>
``rematch2`` is an experimental [spaCy](https://spacy.io) open-source library and associated tools for performing multilingual rule-based Named Entity Recognition (NER) on abstracts and texts relating to archaeological investigations. The library and tools were created by [University of South Wales Hypermedia Research Group](https://hypermedia.research.southwales.ac.uk/) as part of the [ARIADNEplus project](https://ariadne-infrastructure.eu/).

### Supported Languages <a class="anchor" id="languages"></a>
The languages (currently) supported by the ``rematch2`` pipeline components are: 

* German
* English
* Spanish
* French
* Italian
* Dutch
* Norwegian
* Swedish

## Patterns <a class="anchor" id="patterns"></a>
The pipeline components are located in the *components* directory. The components utilise spaCy *patterns* located in the *patterns* directory, these are python modules using the naming convention ``patterns_{language}_{ENTITYTYPE}.py`` e.g. ``patterns_en_YEARSPAN.py``. For further details on the syntax of patterns see [spaCy rule-based matching](https://spacy.io/usage/rule-based-matching).

## Components <a class="anchor" id="components"></a>
### Temporal Components <a class="anchor" id="temporal_components"></a>
``rematch2`` performs specialised NER focussed on temporal entities, and implements specialised spaCy pipeline components to identify the following entity types in free text:

| Component Name        | Entity Type | Description | Examples |
| ----------------------|-------------|-------------| --------:|
| [dayname_ruler](#dayname_ruler)     | DAYNAME     | Day names and their common abbreviations | *Mon., TUES, Wednesday* |
| [monthname_ruler](#monthname_ruler)   | MONTHNAME   | Month names and their common abbreviations | *Jan., FEB, March* |
| [seasonname_ruler](#seasonname_ruler)  | SEASONNAME  | Season names | *Spring, SUMMER, Autumn, WINTER, Fall* |
| [ordinal_ruler](#ordinal_ruler)     | ORDINAL     | Expressions of ordinals (used in identifying centuries) | *1st, first, THIRD, 3RD* |
| [dateprefix_ruler](#dateprefix_ruler)  | DATEPREFIX  | Prefixes commonly associated with years, spans and centuries | *Circa, Early, earlier, mid, MIDDLE, Late, later* |
| [datesuffix_ruler](#datesuffix_ruler)  | DATESUFFIX  | Prefixes commonly associated with years, spans and centuries | *A.D., AD, B.C., BC, B.P., BP* |
| [century_ruler](#century_ruler)     | CENTURY     | Ordinal century expression | *early 15th century BC to late fifteenth century AD* |
| [yearspan_ruler](#yearspan_ruler)    | YEARSPAN    | Spans of years (possibly with prefixes and/or suffixes) | *early 1300 to late 1350 AD* |
| [namedperiod_ruler](#namedperiod_ruler) | NAMEDPERIOD | Period label from a specified [Perio.do](https://perio.do/en/) authority | *Bronze Age, Early Medieval, Victorian* |

### dayname_ruler <a class="anchor" id="dayname_ruler"></a>
Identifies day names or their abbreviations in text. Not currently used by other rulers, but remains present and usable as a concrete example showing how to implement a custom multilingual entity recognition pattern ruler.

### monthname_ruler <a class="anchor" id="monthname_ruler"></a>
Identifies month names or their abbreviations in text. Used in combination with other rulers to identify pattern of month followed by year e.g. *June 1867*

### seasonname_ruler <a class="anchor" id="seasonname_ruler"></a>
Identifies season names in text. Used in combination with other rulers to identify pattern of season followed by year e.g. *Spring 1867*

### ordinal_ruler <a class="anchor" id="ordinal_ruler"></a>
Identifies ordinal expressions in text e.g. *15th, nineteenth*. Used in combination with other rulers to identify pattern of ordinal followed by century e.g. *15th century*, *nineteenth century*. As an alternative spaCy does have its own built in NER functionality which includes identification of ordinals; these patterns were developed prior to adopting spaCy

### dateprefix_ruler <a class="anchor" id="dateprefix_ruler"></a>
Identifies typical dating prefixes in text. Used in combination with other rulers to identify patterns of prefixes followed by century or year e.g. *early 1867*, *circa mid 19th century*

### datesuffix_ruler <a class="anchor" id="datesuffix_ruler"></a>
Identifies typical dating suffixes in text. Used in combination with other rulers to identify patterns of year or century followed by suffix e.g. *early 1867 AD*, *5th century BC*

### century_ruler <a class="anchor" id="century_ruler"></a>
Identifies typical expressions of centuries or spans of centuries in text. Utilises other rulers to identify more complex patterns e.g. *circa early 5th to late fourth century BC*  

### yearspan_ruler <a class="anchor" id="yearspan_ruler"></a>
Identifies typical expressions of years or spans of years in text. Utilises other rulers to identify more complex patterns e.g. *late 1712 to early 1714 AD*

### namedperiod_ruler <a class="anchor" id="namedperiod_ruler"></a>
The namedperiod_ruler component utilises the [Perio.do](https://perio.do/) dataset. When configured with a valid Perio.do authority identifier e.g. `'p0xxt6t'` [Scottish Archaeological Periods & Ages (ScAPA)](http://n2t.net/ark:/99152/p0xxt6t), the component will match against the labels of periods contained within the specified authority. e.g. *Chalcolithic*, *Early Bronze Age*, *Antonine*

These components are pulled together in the TemporalAnnotator class, which facilitates annotation of text using specified combinations of the components. Practical interactive examples of usage are found in the accompanying Python notebooks. 

### Supplementary Components <a class="anchor" id="supplementary_components"></a>
In addition to temporal entities, ``rematch2`` also contains vocabulary-based pipeline components for matching on archaeological vocabulary terms. Note these pipeline components are based on monolingual (English) thesauri so they can only (currently) be used to identify English language terms:

| Component Name     | Entity Type   | Description   | Examples  |
|--------------------|---------------|---------------| ----------|
| [archscience_ruler](#archscience_ruler) | ARCHSCIENCE  | Matching on terms from the [FISH Archaeological Sciences Thesaurus](http://purl.org/heritagedata/schemes/560) | *lead isotope dating, palynology* |
| [material_ruler](#material_ruler) | MATERIAL  | Matching on terms from the [FISH Building Materials Thesaurus](http://purl.org/heritagedata/schemes/eh_tbm) | *brass, quartz, pine, bone, leather* |
| [monument_ruler](#monument_ruler) | MONUMENT     | Matching on terms from the [FISH Thesaurus of Monument Types](http://purl.org/heritagedata/schemes/eh_tmt2) | *midden, weighbridge, kiln* |

### archscience_ruler <a class="anchor" id="archscience_ruler"></a>
xx

### material_ruler <a class="anchor" id="material_ruler"></a>
xx

### monument_ruler <a class="anchor" id="monument_ruler"></a>
xx

## Usage <a class="anchor" id="component_usage"></a>
Example Python script to perform NER using a ``rematch2`` pipeline component: 

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

These components are pulled together in the VocabularyAnnotator class, which facilitates annotation of text using specified combinations of the components. Practical interactive examples of usage are found in the accompanying Python notebooks. 
