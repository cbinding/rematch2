# experimentation - identifying 'paired' entities
# e.g. medieval furrow, iron age barrow, Roman villa etc.
from datetime import datetime as DT     # For measuring elapsed time
import itertools  # for product
import pandas as pd
import spacy
from spacy.tokens import Doc
from spacy.matcher import DependencyMatcher
from test_examples_english import test_examples_english
from test_examples_oasis import test_examples_oasis
from collections.abc import MutableSequence
from rematch2.NamedPeriodRuler import create_namedperiod_ruler
from rematch2.VocabularyRuler import create_fish_monument_types_ruler

from lxml import etree as ET


class LogFile:

    def __init__(self, file_name: str = "", clear_previous: bool = True):
        self.file_path = "results.txt"

        if len(file_name.strip()) > 0:
            self.file_path = file_name.strip()
        if (clear_previous):
            self.clear()

    def clear(self):
        with open(self.file_path, "w") as f:
            f.write("")

    def append(self, s: str, print_to_screen: bool = True):
        with open(self.file_path, "a") as f:
            f.write("\n" + s)
        if (print_to_screen):
            print("\n" + s)


def get_pipeline(periodo_authority_id: str = ""):
    # use predefined spaCy pipeline, disable default NER component
    nlp = spacy.load("en_core_web_sm", disable=['ner'])

    # add rematch2 component(s) to the end of the pipeline
    nlp.add_pipe("namedperiod_ruler", last=True, config={
        "periodo_authority_id": periodo_authority_id})
    nlp.add_pipe("fish_archobjects_ruler", last=True)
    nlp.add_pipe("fish_monument_types_ruler", last=True)
    return nlp


def find_period_object_pairs(nlp=None, periodo_authority_id: str = "", input_text: str = "") -> str:
    results = ""

    # normalise white space before annotation
    # (extra spaces frustrate pattern matching)
    cleaned = " ".join(input_text.strip().split())

    # get predefined spaCy pipeline (if not passed in)
    if (nlp is None):
        nlp = get_pipeline(periodo_authority_id)

    # perform the annotation
    doc = nlp(cleaned)

    results += "=============================================================\n"
    results += f"input text:\n\"{input_text}\"\n"
    results += get_entity_occurrence_counts(doc)

    results += "\nNoun chunk pairs [PERIOD - OBJECT]:\n"
    pairs = get_noun_chunk_pairs(doc)
    if len(pairs) == 0:
        results += "NONE FOUND\n"
    else:
        for ent1, ent2 in pairs:
            results += f"[{ent1.ent_id_}] '{ent1}' - '{ent2}' [{ent2.ent_id_}]\n"

    # semgrex symbols for dependency relationship between terms
    # see https://spacy.io/usage/rule-based-matching#dependencymatcher-operators
    for rel_op in [
        "<",    # A is the immediate dependent of B
        ">",    # A is the immediate head of B
        "<<",   # A is the dependent in a chain to B following dep → head paths
        ">>",   # A is the head in a chain to B following head → dep paths
        ".",    # A immediately precedes B, i.e. A.i == B.i - 1, and both are within the same dependency tree
        ".*",   # A precedes B, i.e. A.i < B.i, and both are within the same dependency tree
        ";",    # A immediately follows B, i.e. A.i == B.i + 1, and both are within the same dependency tree
        ";*",   # A follows B, i.e. A.i > B.i, and both are within the same dependency tree
        "$+",   # B is a right immediate sibling of A, i.e. A and B have the same parent and A.i == B.i - 1
        "$-",   # B is a left immediate sibling of A, i.e. A and B have the same parent and A.i == B.i + 1
        "$++",  # B is a right sibling of A, i.e. A and B have the same parent and A.i < B.i
        "$--",  # B is a left sibling of A, i.e. A and B have the same parent and A.i > B.i
        ">+",   # B is a right immediate child of A, i.e. A is a parent of B and A.i == B.i - 1
        ">-",   # B is a left immediate child of A, i.e. A is a parent of B and A.i == B.i + 1
        ">++",  # B is a right child of A, i.e. A is a parent of B and A.i < B.i
        ">--",  # B is a left child of A, i.e. A is a parent of B and A.i > B.i
        "<+",   # B is a right immediate parent of A, i.e. A is a child of B and A.i == B.i - 1
        "<-",   # B is a left immediate parent of A, i.e. A is a child of B and A.i == B.i + 1
        "<++",  # B is a right parent of A, i.e. A is a child of B and A.i < B.i
        "<--"   # B is a left parent of A, i.e. A is a child of B and A.i > B.i
    ]:
        # print(get_dependency_match_pairs(doc, rel_op))
        results += f"\nDependency matched pairs [PERIOD {rel_op} OBJECT]:\n"
        pairs = get_dependency_match_pairs(doc, rel_op)
        if len(pairs) == 0:
            results += "NONE FOUND\n"
        else:
            for ent1, ent2 in pairs:
                results += f"[{ent1.ent_id_}] '{ent1}' - '{ent2}' [{ent2.ent_id_}]\n"
    return results


def get_entity_occurrence_counts(doc: Doc) -> str:

    # load ents into a DataFrame object:
    pd.set_option('display.max_rows', None)
    df = pd.DataFrame([{
        "from": ent.start_char,
        "to": ent.end_char - 1,
        "id": ent.ent_id_,
        "text": ent.text,
        "lemma": ent.lemma_.lower(),
        "orth": ent.orth_,
        "type": ent.label_
    } for ent in doc.ents])

    # summarise identified entities
    result = "\nOccurrence counts:\n"
    result += str(df.groupby(["id", "lemma", "type"]
                             ).size().sort_values(ascending=False))
    return result


# using dependency matcher..
# https://spacy.io/usage/rule-based-matching#dependencymatcher
# look for PERIOD - OBJECT dependency pairs, return as tuple array [[ent, ent], [ent, ent]]
def get_dependency_match_pairs(doc: Doc, rel_op: str = ".") -> MutableSequence:
    pattern = [
        {
            "RIGHT_ID": "period",
            "RIGHT_ATTRS": {"ENT_TYPE": "NAMEDPERIOD"}
        },
        {
            "LEFT_ID": "period",
            "REL_OP": rel_op,
            "RIGHT_ID": "object",
            "RIGHT_ATTRS": {"ENT_TYPE": "OBJECT"}
        }
    ]
    matcher = DependencyMatcher(doc.vocab)
    matcher.add("PERIOD_OBJECT", [pattern])
    matches = matcher(doc)

    matched = dict()
    for match_id, token_ids in matches:
        # get all NAMEDPERIOD entities token_ids match
        periods = filter(lambda ent: ent.label_ == "NAMEDPERIOD" and any(
            ent.start <= id and ent.end > id for id in token_ids), doc.ents)
        # get all OBJECT entities token_ids match
        objects = filter(lambda ent: ent.label_ == "OBJECT" and any(
            ent.start <= id and ent.end > id for id in token_ids), doc.ents)
        # using cartesian product to give all PERIOD - OBJECT pair combinations
        for ent1, ent2 in itertools.product(periods, objects):
            # using dict to eliminate duplicate pairs
            matched[f"{ent1.ent_id_}{ent2.ent_id_}"] = tuple([ent1, ent2])
    # return as array of tuple
    return matched.values()


# look for PERIOD - OBJECT pairs in noun chunks,
# return as tuple array [[ent, ent], [ent, ent]]
def get_noun_chunk_pairs(doc: Doc) -> MutableSequence:
    '''
    # load noun chunks into a DataFrame object    
    pd.set_option('display.max_rows', None)
    df = pd.DataFrame([{
        "from": chunk.start_char,
        "to": chunk.end_char - 1,
        "id": chunk.ent_id_,
        "text": chunk.text,
        "ents": chunk.ents
    } for chunk in doc.noun_chunks])
    # print("noun chunks:")
    # print(df)
    '''

    # looking for PERIOD - OBJECT pairs within noun chunks
    # result += f"Noun chunk pairs [PERIOD - OBJECT]:"
    matched = dict()
    for chunk in doc.noun_chunks:
        # get all NAMEDPERIOD entities in the noun chunk
        periods = filter(lambda ent: ent.label_ == "NAMEDPERIOD", chunk.ents)
        # get all OBJECT entities in the noun chunk
        objects = filter(lambda ent: ent.label_ == "OBJECT", chunk.ents)
        # Use cartesian product to give all PERIOD - OBJECT pairs
        for ent1, ent2 in itertools.product(periods, objects):
            # using dict to eliminate duplicate pairs
            matched[f"{ent1.ent_id_}{ent2.ent_id_}"] = tuple([ent1, ent2])
            # result += f"\n[{ent1.ent_id_}] '{ent1}' - '{ent2}' [{ent2.ent_id_}]"
     # return as array of tuple
    return matched.values()

# run using limited oasis test examples


def main1():
    # create log file to report results
    log = LogFile(f"find_pairs_results_{dt_start.strftime('%Y-%m-%d')}.txt")

    # write header information to screen
    dt_start = DT.now()

    log.append(
        f"{__file__} started at {dt_start.strftime('%Y-%m-%dT%H:%M:%S')}")

    # example test text from https://doi.org/10.5284/1100093
    # input_text = """This collection comprises site data(reports, images, spreadsheets, GIS data and site records) from two phases of archaeological evaluation undertaken by Oxford Archaeology in June 2018 (SAWR18) and February 2021 (SAWR21) at West Road, Sawbridgeworth, Hertfordshire. SAWR18 In June 2018, Oxford Archaeology were commissioned by Taylor Wimpey to undertake an archaeological evaluation on the site of a proposed housing development to the north of West Road, Sawbridgeworth(TL 47842 15448). A programme of 19 trenches was undertaken to ground truth the results of a geophysical survey and to assess the archaeological potential of the site. The evaluation confirmed the presence of archaeological remains in areas identified on the geophysics. Parts of a NW-SE‐aligned trackway were found in Trenches 1 and 2. Field boundaries identified by geophysics(also present on the 1839 tithe map) were found in Trenches 5 and 7, towards the south of the site, and in Trenches 12 and 16, in the centre of the site. Geophysical anomalies identified in the northern part of the site were investigated and identified as geological. The archaeology is consistent with the geophysical survey results and it is likely that much of it has been truncated by modern agricultural activity. SAWR21 Oxford Archaeology carried out an archaeological evaluation on the site of proposed residential development north of West Road, Sawbridgeworth, Hertfordshire, in February 2021. The fieldwork was commissioned by Taylor Wimpey as a condition of planning permission. Preceding geophysical survey of the c 5.7ha development site was undertaken in 2016 and identified a concentration of linear and curvilinear anomalies in the north-east corner of the site and two areas of several broadly NW-SE aligned anomalies in the southern half of the site. Subsequent trial trench evaluation, comprising the investigation of 19 trenches, was undertaken by Oxford Archaeology in 2018, targeted upon the geophysical survey results. The evaluation revealed a small number of ditches in the centre and south of the site, correlating with the geophysical anomalies. Although generally undated, the ditches were suggestive of a trackway and associated enclosure/field boundaries. Other ditches encountered on site correlated with post-medieval field boundaries depicted on 19th century mapping. Given the results of the 2018 evaluation, in conjunction with those of the 2018 investigations at nearby Chalk's Farm, which uncovered the remains of Late Bronze Age early Iron Age and early Roman settlement and agricultural activity, it was deemed necessary to undertake a further phase of
    # evaluation at the site. An Early Roman aesica brooch was found. Four additional trenches were excavated in the southern half of the site to further investigate the previously revealed ditches. The continuations of the trackway ditches were revealed in the centre of the site, with remnants of a metalled surface also identified. Adjacent ditches may demonstrate the maintenance and modification of the trackway or perhaps associated enclosure/field boundaries. Artefactual dating evidence recovered from these ditches was limited and of mixed date, comprising small pottery sherds of late Bronze Age-early Iron Age date and fragments of Roman ceramic building material. It is probable that these remains provide evidence of outlying agricultural activity associated with the later prehistoric and early Roman settlement evidence at Chalk's Farm. A further undated ditch and a parallel early Roman ditch were revealed in the south of the site, suggestive of additional land divisions, probably agricultural features. A post-medieval field boundary ditch and modern land drains are demonstrative of agricultural use of the landscape during these periods."""

    # set up configured pipeline once rather than per record (faster?)
    nlp = get_pipeline(periodo_authority_id="p0kh9ds")

    for example in test_examples_oasis:
        input_text = example.get("text", "")
        log.append(find_period_object_pairs(
            nlp=nlp, periodo_authority_id="p0kh9ds", input_text=input_text))

        # find_period_object_pairs(
        # periodo_authority_id="p0kh9ds", input_text=test_examples_english[9].get("text", ""))

        # find_period_monument_pairs(
        # periodo_authority_id="p0kh9ds", input_text=test_examples_english[5].get("text", ""))

        # Finished - write footer information to screen
    dt_end = DT.now()
    log.append(
        f"{__file__} finished at {dt_start.strftime('%Y-%m-%dT%H:%M:%S')}")
    duration = dt_end - dt_start
    log.append(f"finished in {duration}")


# run using XML file of OASIS abstracts (oasis_descr_examples.xml)
def main2():
    # OASIS example data received from Tim @ ADS
    sourceFilePath = "./oasis_descr_examples.xml"

    # create log file to report results
    log = LogFile(f"find_pairs_results_{dt_start.strftime('%Y-%m-%d')}.txt")
    
    # write header information to log
    dt_start = DT.now()
    log.append(f"Input data file path: '{sourceFilePath}'")    
    log.append(
        f"{__file__} started at {dt_start.strftime('%Y-%m-%dT%H:%M:%S')}")

    
    try:
        # read XML file
        tree = ET.parse(sourceFilePath)
        root = tree.getroot()
    except:
        print(f"Could not read from {sourceFilePath}")
        return 0

    # set up configured pipeline once only (faster than per record)
    nlp = get_pipeline(periodo_authority_id="p0kh9ds")

    # find records to be processed in the XML file
    # xpathRecords = "/Collections/records/record"
    xpathRecords = "/table/rows/row"  
    print(f"looking for xpath {xpathRecords}")
    records = tree.xpath(xpathRecords)
    
    # print number of records found 
    totalRecords = len(records)
    print(f"found {totalRecords} records")
    
    # process each record
    currentRecord = 0
    for record in records:
        # find abstract(s) in the current record
        # abstracts = record.xpath('dc:description/text()',
        # namespaces={'dc': 'http://purl.org/dc/elements/1.1/'}) 
        abstracts = record.xpath("value[@columnNumber='1']/text()")
        # find identifier(s) in the current record
        # identifiers = record.xpath('dc:source/text()',
        # namespaces={'dc': 'http://purl.org/dc/elements/1.1/'})
        identifiers = record.xpath("value[@columnNumber='0']/text()")

        # if multiple abstracts for record, get first one
        if (len(abstracts) > 0):
            abstract = abstracts[0]
        else:
            abstract = ""

        # if multiple identifiers for record, get first one
        # and remove URL prefix if present
        if (len(identifiers) > 0):
            identifier = identifiers[0]
            identifier = identifier.replace(
                "https://archaeologydataservice.ac.uk/archsearch/record?titleId=", "")
        else:
            identifier = ""

        # process this abstract
        log.append(f"ID: {identifier}")
        log.append(find_period_object_pairs(
            nlp=nlp, periodo_authority_id="p0kh9ds", input_text=abstract.lower()))

    # finished - write footer information to log
    dt_end = DT.now()
    log.append(
        f"{__file__} finished at {dt_start.strftime('%Y-%m-%dT%H:%M:%S')}")
    duration = dt_end - dt_start
    log.append(f"finished in {duration}")


if __name__ == '__main__':
    main2()
