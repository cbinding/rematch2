# experimentation - identifying 'paired' entities
# e.g. medieval furrow, iron age barrow, Roman villa etc.
import itertools  # for product
import pandas as pd
import spacy
from spacy.tokens import Doc
from spacy.matcher import DependencyMatcher
from test_examples_english import test_examples_english
from test_examples_oasis import test_examples_oasis
from collections.abc import MutableSequence
from rematch2.NamedPeriodRuler import create_namedperiod_ruler
from rematch2.VocabularyRuler import *
from lxml import etree as ET

from decorators import run_timed

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


# parse out list of records from the source XML file [{"id", "text"}, {"id", "text"}] 
# ready for subsequent processing
def get_records_from_xml_file(file_path: str="")-> list:
    try:
        # read XML file
        tree = ET.parse(file_path)
        root = tree.getroot()
    except:
        print(f"Could not read from {sourceFilePath}")
        return 0

    records = []

    # find items to be processed in the XML file
    rows = tree.xpath("/table/rows/row")

    for row in rows:
        # find abstract(s) in the current record
        abstracts = row.xpath("value[@columnNumber='1']/text()")
       
        # if multiple abstracts for record, get first one
        if (len(abstracts) > 0):
            abstract = abstracts[0]
        else:
            abstract = ""

         # find identifier(s) in the current record
        identifiers = row.xpath("value[@columnNumber='0']/text()")

        # if multiple identifiers for record, get first one (and remove URL prefix if present)
        if (len(identifiers) > 0):
            identifier = identifiers[0]
            identifier = identifier.replace(
                "https://archaeologydataservice.ac.uk/archsearch/record?titleId=", "")
        else:
            identifier = ""

        ## create new (data cleaned) record and add it
        record = {}
        record["id"] = identifier.strip()
        record["text"] = abstract.strip()
        records.append(record)

    

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
    result += str(df.groupby(["id", "lemma", "type"]).size().sort_values(ascending=False))
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





# run using list of [{"id", "text"},{"id", "text"}]
@run_timed
def main(records, log=None):       
     # print number of records found 
    print(f"processing {len(records)} records")
    
    # set up configured pipeline once only (faster than per record)
    nlp = get_pipeline(periodo_authority_id="p0kh9ds")    

     # process each record
    currentRecord = 0
    for record in records:        

        # process this record
        identifier = record.get("id", "")
        input_text = record.get("text", "")
        if log is not None:
            log.append(f"ID: {identifier}")
            log.append(find_period_object_pairs(
                nlp=nlp, periodo_authority_id="p0kh9ds", input_text=input_text.lower()))


if __name__ == '__main__':

    log = LogFile("find_pairs_results.txt")
    from_xml = False

    if(from_xml):
        # get list of records to be processed [{"id", "text"},{"id", "text"}]
        # (XML file is OASIS example data received from Tim @ ADS)      
        records = get_records_from_xml_file("./oasis_descr_examples.xml")
    else:
        # example records for testing
        records = test_examples_oasis    
    
    main(records, log)
