"""
=============================================================================
Package :   rematch2
Module  :   MonumentRuler.py
Version :   20220803
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   ARIADNEplus
Summary :   spaCy custom pipeline component (specialized EntityRuler)
Imports :   os, sys, spacy, EntityRuler, Doc, Language
Example :   nlp.add_pipe("monument_ruler", last=True);
            draws on https://github.com/ICLRandD/Blackstone/blob/master/blackstone/pipeline/concepts.py            
License :   https://creativecommons.org/licenses/by/4.0/ [CC-BY]
History :   03/08/2022 CFB Initially created script
=============================================================================
""" 
import os
import sys
import spacy            # NLP library

from spacy.language import Language
#from spacy.lang.de import German
from spacy.lang.en import English
from spacy.lang.fr import French

from spacy.pipeline import EntityRuler
from spacy.tokens import Doc

#from collections import Counter
#from patterns import patterns_de_MONUMENT
from patterns import patterns_en_MONUMENT
#from patterns import patterns_fr_MONUMENT


module_path = os.path.abspath(os.path.join('..', 'src'))
if module_path not in sys.path:
    sys.path.append(module_path)


@Language.factory("monument_ruler")
def create_monument_ruler(nlp, name, patterns):   
    return MonumentRuler(nlp, name, patterns)      
    

@English.factory("monument_ruler")
def create_monument_ruler_en(nlp, name):
    ruler = create_monument_ruler(nlp, name, patterns_en_MONUMENT)
    return ruler


@French.factory("monument_ruler")
def create_monument_ruler_fr(nlp, name):
    ruler = create_monument_ruler(nlp, name, patterns_en_MONUMENT) # TODO - use INRAP/PACTOLS patterns here...
    return ruler


"""
@German.factory("monument_ruler")
def create_monument_ruler_de(nlp, name):
    patterns = patterns_de_MONUMENT
    return MonumentRuler(nlp, name, patterns)
"""

# MonumentRuler is a specialized EntityRuler
class MonumentRuler(EntityRuler): 
    def __init__(self, nlp: Language, name: str, patterns=[]) -> None:
        EntityRuler.__init__(
            self, 
            nlp=nlp, 
            name=name,
            phrase_matcher_attr="LOWER",
            validate=True,
            overwrite_ents=True,
            ent_id_sep="||",
            patterns = patterns
        )    

    # in this instance we just call the parent function, 
    # but could do more doc processing here
    def __call__(self, doc: Doc) -> Doc:
        EntityRuler.__call__(self, doc)
        return doc


# test the monument_ruler pipeline component
if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm", disable = ['ner']) 
    nlp.add_pipe("monument_ruler", last=True)  
    print(nlp.pipe_names) 
    text = "Underlying the modern made ground on the site was a layer covering the entire shaft area. This has been dated to c.1480-1800/1900 and interpreted as a post-medieval cultivation soil. Historic mapping illustrates that the site remained undeveloped through the post medieval period until the mid-19th century, when urban development around the site accelerated and construction of railways in this part of London began. On Gascoigne's 1703 map the site was open ground, the later maps of Rocque in 1746 and Horwood in 1799 show the area was in use as fields and Stanford's map of 1862 depicts the area surrounding Eleanor Street comprising of market gardens. These are all consistent with the archaeological evidence. Underlying the layer were natural terrace gravels. The archaeological fieldwork has demonstrated that remains relating to the Prehistoric, Roman or medieval period have not survived to the modern era, if they were once present on site."
    doc = nlp(text)
    for ent in doc.ents:
        print (ent.ent_id_, ent.text, ent.label_)
    


    