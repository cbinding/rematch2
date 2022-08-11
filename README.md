# rematch2

## Introduction
``rematch2`` is an experimental [spaCy](https://spacy.io) open-source library and associated tools for performing multilingual rule-based Named Entity Recognition (NER) on abstracts and texts relating to archaeological investigations. The library and tools were created by [University of South Wales Hypermedia Research Group](https://hypermedia.research.southwales.ac.uk/) as part of the [ARIADNEplus project](https://ariadne-infrastructure.eu/). 

## Named Entity Recognition
``rematch2`` performs specialised NER focussed on temporal entities, and implements spaCy pipeline components to identify the following entity types in free text:

| Component Name       | Entity Type   | Description | Examples  |
| ---------------------|---------------|-------------| ----------|
| ``dayname_ruler``    | DAYNAME       | Day names and their common abbreviations | Mon., TUES, Wednesday |
| ``monthname_ruler``  | MONTHNAME     | Month names and their common abbreviations | Jan., FEB, March |
| ``seasonname_ruler`` | SEASONNAME    | Season names | Spring, SUMMER, Autumn, WINTER, Fall |
| ``ordinal_ruler`` | ORDINAL       | Expressions of ordinals (used in identifying centuries) | 1st, first, THIRD, 3RD |
| ``dateprefix_ruler`` | DATEPREFIX    | Prefixes commonly associated with years, spans and centuries | Circa, Early, earlier, mid, MIDDLE, Late, later |
| ``datesuffix_ruler`` | DATESUFFIX    | Prefixes commonly associated with years, spans and centuries | A.D., AD, B.C., BC, B.P., BP |
| ``yearspan_ruler``   | YEARSPAN      | Spans of years (possibly with prefixes and/or suffixes) | early 1300 to late 1350 AD |
| ``century_ruler``    | CENTURY       | Ordinal century expression | early 15th century BC to late fifteenth century AD |
| ``namedperiod_ruler`` | NAMEDPERIOD   | Period label from a specified [Perio.do](https://perio.do/en/) authority | Bronze Age, Early Medieval, Victorian |

## Supported languages
The languages currently supported by the pipeline components are: 

* German (de)
* English (en)
* Spanish (es)
* French (fr)
* Italian (it)
* Dutch (nl)
* Norwegian (no)
* Swedish (sv)

## Usage
To perform NER using a ``rematch2`` pipeline component: 

```python
#!/usr/bin/env python3
import spacy
from rematch2.components import create_century_ruler

# use a predefined pipeline, disabling the built-in NER component
nlp = spacy.load("en_core_web_sm", disable = ['ner'])
# add required pipe component to the end of the pipeline
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

## Patterns
The pipeline components can be found in the *components* directory. These utilise corresponding spaCy *patterns*, which can be found within the *patterns* directory. The files in the *patterns* directory are python modules using the naming convention ``patterns_{language}_{ENTITYTYPE}.py`` e.g. ``patterns_en_YEARSPAN.py``.

### Supplementary NER pipeline components
In addition to temporal entities, ``rematch2`` also contains some more experimental vocabulary-based pipeline components for matching on archaeological vocabulary terms. Note these pipeline components are based on monolingual (English) thesauri so they can only (currently) be used to identify English language terms:

| Component Name     | Entity Type   | Description   | Examples  |
|--------------------|---------------|---------------| ----------|
| ``material_ruler`` | MATERIAL  | Terms from the [FISH Building Materials Thesaurus](http://purl.org/heritagedata/schemes/eh_tbm) | brass, quartz, pine, bone, leather |
| ``archscience_ruler`` | MONUMENT     | Terms from the [FISH Thesaurus of Monument Types](http://purl.org/heritagedata/schemes/eh_tmt2) | midden, weighbridge, kiln |
| ``monument_ruler`` | ARCHSCIENCE  | Terms from the [FISH Archaeological Sciences Thesaurus](http://purl.org/heritagedata/schemes/560) | lead isotope dating, palynology |

