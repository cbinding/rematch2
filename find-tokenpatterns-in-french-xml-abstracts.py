# =============================================================================
# Project   : ARIADNEplus
# Package   : NLP
# Module    : find-tokenpatterns-in-french-xml-abstracts.py
# Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
# Contact   : ceri.binding@southwales.ac.uk
# Summary   :
#    Bulk processing script identifies matching token patterns
#    in French report abstracts contained in XML metadata file
# Imports   : spacy
# Example   :
#  python3 find-tokenpatterns-in-french-xml-abstracts.py -i "path/to/abstracts/file.xml"
# License   : https://github.com/cbinding/rematch2/blob/main/LICENSE.txt
# =============================================================================
# History
# 06/08/2021 CFB Initially created script
# 30/09/2022 CFB recreated to run using rematch2 library (Perio.do periods)
# 21/11/2022 CFB Using rematch2.TemporalAnnotator object, faster
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
from rematch2 import TemporalAnnotator


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
            "CENTURY",
            "NAMEDPERIOD",
            "YEARSPAN"
        ],
        "colors": {
            "CENTURY": "lightgreen",
            "NAMEDPERIOD": "yellow",
            "YEARSPAN": "salmon"
        }
    }
    html = displacy.render([doc], style="ent", page=True,
                           minify=True, options=options)

    with open(targetFileNameWithPath, 'w', encoding='utf-8-sig') as f:
        f.write(html)


def main(sourceFilePath):

    annotator = TemporalAnnotator(
        language="fr", periodo_authority_id="p02chr4")

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
    xpathRecords = "./UNIMARC"
    xpathRecordAbstract = "XML_FIELD/MARC/_330/_330a"
    xpathRecordIdentifier = "XML_FIELD/MARC/_900/_900a"

    print(f"looking for {xpathRecords}")
    records = root.findall(xpathRecords)
    totalRecords = len(records)
    print(f"Found {totalRecords} records")

    currentRecord = 0
    for record in records:
        abstracts = record.findall(xpathRecordAbstract)
        identifiers = record.findall(xpathRecordIdentifier)
        if(len(abstracts) > 0):
            abstract = abstracts[0].text
        else:
            abstract = ""
        if(len(identifiers) > 0):
            identifier = identifiers[0].text
        else:
            identifier = ""

        #print(f"Identifier: {identifier}\nAbstract:\n{abstract}\n*****\n")

        doc = annotator.annotateText(input_text=abstract, format="doc")

        # write results to JSON file.
        now = DT.now()
        ents = []
        for ent in doc.ents:
            ents.append({
                "text": ent.text,
                "start": ent.start_char,
                "end": ent.end_char,
                "type": ent.label_
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
        sourceFilePath = "ner-fr/UNIMARC.xml"  # temp harcoded test..

    main(sourceFilePath)
