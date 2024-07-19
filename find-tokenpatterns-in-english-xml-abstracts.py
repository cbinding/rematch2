# =============================================================================
# Project   : Enrich
# Package   : NER
# Module    : find-tokenpatterns-in-english-xml-abstracts.py
# Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
# Contact   : ceri.binding@southwales.ac.uk
# Summary   : Identifies matching token patterns in English text
# Imports   : spacy rematch2.VocabularyAnnotator
# Example   : python en-find-tokenpatterns-in-xml-abstracts.py -i "path/to/abstracts/file.xml"
# License   : http://creativecommons.org/publicdomain/zero/1.0/ [CC0]
# =============================================================================
# History
# 01/09/2021 CFB Initially created script
# 03/02/2023 CFB Adapted to use new rematch2 components
# =============================================================================
import argparse                         # for argument parsing
import os                               # for general file/directory functionality
from datetime import datetime as DT     # For timestamps and durations

import re
import json
from lxml import etree as ET
from collections import defaultdict
import spacy
from spacy import displacy
from rematch2.VocabularyAnnotator import VocabularyAnnotator


def writeEntitiesToTsvFile(doc, targetFileNameWithPath="", mode="w"):
    writeEntitiesToDelimitedFile(doc, targetFileNameWithPath, "\t", mode)


def writeEntitiesToDelimitedFile(doc, targetFileNameWithPath="", delimiter="\t", mode="w"):
    txt = ""
    for ent in doc.ents:
        txt += f"{ent.ent_id_}{delimiter}{ent.text}{delimiter}{ent.start_char}{delimiter}{ent.end_char}{delimiter}{ent.label_}\n"

    with open(targetFileNameWithPath, mode, encoding='utf-8-sig') as f:
        f.write(txt)


def writeEntitiesToHtmlFile(doc, targetFileNameWithPath=""):
    options = {
        "ents": [
            "YEARSPAN",
            "PERIOD",
            "FISH_MONUMENT",
            "FISH_OBJECT",
            "FISH_ARCHSCIENCE",
            "FISH_EVIDENCE",
            "FISH_MATERIAL",
            "FISH_EVENTTYPE"
        ],
        "colors": {
            "YEARSPAN": "moccasin",
            "PERIOD": "yellow",
            "FISH_MONUMENT": "cyan",
            "FISH_OBJECT": "plum",
            "FISH_ARCHSCIENCE": "pink",
            "FISH_EVIDENCE": "aliceblue",
            "FISH_MATERIAL": "antiquewhite",
            "FISH_EVENTTYPE": "coral",
        }
    }
    html = displacy.render([doc], style="ent", page=True,
                           minify=True, options=options)

    with open(targetFileNameWithPath, 'w', encoding='utf-8-sig') as f:
        f.write(html)


def main(sourceFilePath):
    print(f"running main({sourceFilePath})")
    annotator = VocabularyAnnotator(
        language="en", periodo_authority_id="p0kh9ds", labels=["OBJECT", "MONUMENT", "PERIOD"])

    results = defaultdict(dict)
    sourceFileDirectory = os.path.dirname(sourceFilePath)

    baseDirectory = os.path.join(sourceFileDirectory, "fromxml")
    if "fromxml" not in os.listdir(sourceFileDirectory):
        os.mkdir(baseDirectory)

    tsvDirectory = os.path.join(baseDirectory, "tsv")
    if "tsv" not in os.listdir(baseDirectory):
        os.mkdir(tsvDirectory)

    htmlDirectory = os.path.join(baseDirectory, "html")
    if "html" not in os.listdir(baseDirectory):
        os.mkdir(htmlDirectory)

    # targetFilePath = f"{sourceFilePath}.output.xml"

    try:
        # read XML file
        tree = ET.parse(sourceFilePath)
        root = tree.getroot()
    except:
        print(f"Could not read from {sourceFilePath}")
        return 0

    # locate the abstracts in the XML file
   # find records to be processed in the XML file
    # xpathRecords = "/Collections/records/record"
    xpathRecords = "/table/rows/row"  # OASIS example data from Tim
    print(f"looking for xpath {xpathRecords}")
    records = tree.xpath(xpathRecords)
    totalRecords = len(records)
    print(f"found {totalRecords} records")

    # process each record located
    currentRecord = 0
    for record in records:
        # find abstract(s) in the current record
        # abstracts = record.xpath('dc:description/text()',
        # namespaces={'dc': 'http://purl.org/dc/elements/1.1/'})
        # find identifier(s) in the current record
        # identifiers = record.xpath('dc:source/text()',
        # namespaces={'dc': 'http://purl.org/dc/elements/1.1/'})
        # OASIS example data from Tim
        abstracts = record.xpath("value[@columnNumber='1']/text()")
        # OASIS example data from Tim
        identifiers = record.xpath("value[@columnNumber='0']/text()")
        if (len(abstracts) > 0):
            abstract = abstracts[0]
        else:
            abstract = ""        

        if (len(identifiers) > 0):
            identifier = identifiers[0]
            identifier = identifier.replace(
                "https://archaeologydataservice.ac.uk/archsearch/record?titleId=", "")
        else:
            identifier = ""

        # print(f"Identifier: {identifier}\nAbstract:\n{abstract}\n*****\n")
        # print(f"abstract: {str(abstract)}")
        doc = annotator.annotateText(input_text=str(abstract), format="doc")

        # write results to JSON file.
        now = DT.now()
        ents = []
        for ent in doc.ents:
            ents.append({
                "text": ent.text,
                "start": ent.start_char,
                "end": ent.end_char,
                "label": ent.label_
            })
        results[identifier]["source"] = sourceFilePath
        results[identifier]["identifier"] = identifier
        results[identifier]["created"] = f"{now.year}-{now.month}-{now.day}"
        results[identifier]["process"] = __file__
        results[identifier]["abstract"] = abstract
        results[identifier]["subjects"] = ents

        currentRecord += 1
        if currentRecord == 10000:  # premature break during testing
            break

        # remove any non-word or non-space characters from ID
        cleanIdentifier = re.sub(r'[^\w\s]', '', identifier)
        print(
            f"processing record { currentRecord } of { totalRecords } [{ identifier }]")

        # append data to 'overall' results TSV file
        tsvOverallFileNameWithPath = os.path.join(
            tsvDirectory, f"output.fromxml.txt")
        delimiter = "\t"
        txt = ""
        for ent in doc.ents:
            txt += f"{identifier}{delimiter}{ent.ent_id_}{delimiter}{ent.text}{delimiter}{ent.label_}\n"
        with open(tsvOverallFileNameWithPath, 'a', encoding='utf-8-sig') as f:
            f.write(txt)

        tsvFileNameWithPath = os.path.join(
            tsvDirectory, f"{cleanIdentifier}.fromxml.txt")
        writeEntitiesToTsvFile(doc, tsvFileNameWithPath)

        htmlFileNameWithPath = os.path.join(
            htmlDirectory, f"{cleanIdentifier}.fromxml.html")
        writeEntitiesToHtmlFile(doc, htmlFileNameWithPath)

    # write results dict to (JSON) file
    jsonFileNameWithPath = f"{sourceFilePath}.json"
    with open(jsonFileNameWithPath, 'w', encoding="utf-8-sig") as file:
        json.dump(results, file, sort_keys=True)


if __name__ == '__main__':

    # initiate the input arguments parser
    parser = argparse.ArgumentParser(
        prog=__file__, description="Find token patterns in XML metadata abstracts")

    # add long and short argument descriptions
    parser.add_argument("--inputfilepath", "-i", required=False,
                        help="Input XML metadata file with path")

    # parse command line arguments
    args = parser.parse_args()

    # clean required arguments
    if args.inputfilepath:
        sourceFilePath = args.inputfilepath.strip()
    else:
        # temp harcoded test..
        sourceFilePath = "./oasis_descr_examples.xml"

    main(sourceFilePath)
