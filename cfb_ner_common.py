# =============================================================================
# Project   : Any
# Package   : NLP
# Module    : cfb_ner_common.py
# Version   : 1.0.0
# Creator   : Ceri Binding, University of South Wales / Prifysgol de Cymru
# Contact   : ceri.binding@southwales.ac.uk
# Summary   : Common code used in NLP/NER work
# Imports   : spacy
# Example   :
# License   : https://creativecommons.org/licenses/by/4.0/ [CC-BY]
# =============================================================================
# History
# 1.0.0 29/09/2021 CFB Initially created script
# =============================================================================
import logging                          # for logging what is going on
from datetime import datetime as DT     # For timestamps and durations
from spacy import displacy
from spacy.matcher import Matcher, PhraseMatcher
from spacy.tokens import Span


def runTimed(func):
    def wrapper(*arg):
        # configure log file
        logging.basicConfig(
            filename="cfb_ner.log",
            filemode='w',
            encoding="utf-8",
            level=logging.DEBUG,
            format='%(asctime)s %(message)s',
            datefmt='%Y-%m-%d %I:%M:%S'
        )

        # log start of execution
        timestampStart = DT.now()
        logging.debug(f"{__file__} started at {timestampStart}")

        func(*arg)

        # Finished. Write footer information to log and screen
        timestampEnd = DT.now()
        duration = timestampEnd - timestampStart
        logging.debug(
            f"{__file__} finished at { timestampEnd } (duration { duration })")

    return wrapper


# returns doc object
def findEntitiesInTextFile(nlp, sourceFileNameWithPath=""):
    with open(sourceFileNameWithPath, 'r', encoding='utf-8-sig') as f:
        txt = f.read()
    doc = findEntitiesInText(nlp, txt)
    return doc


def log(msg):
    logging.debug(msg)
    print(msg)


# write all pattern matches to a delimited file
# todo: escape delimiter if it occurs in the values being written
def writeEntitiesToCsvFile(doc, targetFileNameWithPath="", mode="w"):
    writeEntitiesToDelimitedFile(doc, targetFileNameWithPath, ",", mode)


def writeEntitiesToTsvFile(doc, targetFileNameWithPath="", mode="w"):
    writeEntitiesToDelimitedFile(doc, targetFileNameWithPath, "\t", mode)


def writeEntitiesToDelimitedFile(doc, targetFileNameWithPath="", delimiter="\t", mode="w"):
    txt = ""
    for ent in doc.ents:
        txt += f"{ent.ent_id_}{delimiter}{ent.text}{delimiter}{ent.start_char}{delimiter}{ent.end_char}{delimiter}{ent.label_}\n"

    with open(targetFileNameWithPath, mode, encoding='utf-8-sig') as f:
        f.write(txt)


# write all tokens and POS to a delimited file
# todo: escape delimiter if it occurs in the values being written
def writeTokensToTsvFile(doc, targetFileNameWithPath="", mode="w"):
    writeTokensToDelimitedFile(doc, targetFileNameWithPath, "\t", mode)


def writeTokensToCsvFile(doc, targetFileNameWithPath="", mode="w"):
    writeTokensToDelimitedFile(doc, targetFileNameWithPath, ",", mode)


def writeTokensToDelimitedFile(doc, tokFileNameWithPath, delimiter="\t", mode="w"):
    txt = ""

    for token in doc:
        txt += f"{token.text}{delimiter}{token.pos_}{delimiter}{token.head.text}\n"

    with open(tokFileNameWithPath, mode, encoding='utf-8-sig') as f:
        f.write(txt)


# writes doc matches to HTML
def writeEntitiesToHtmlFile(doc, targetFileNameWithPath="", options={}):

    html = displacy.render([doc], style="ent", page=True,
                           minify=True, options=options)

    with open(targetFileNameWithPath, 'w', encoding='utf-8-sig') as f:
        #f.write("<head><meta charset='UTF-8' /></head>")
        f.write(html)
