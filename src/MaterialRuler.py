"""
=============================================================================
Package :   rematch2
Module  :   MaterialRuler.py
Version :   20220803
Creator :   Ceri Binding, University of South Wales / Prifysgol de Cymru
Contact :   ceri.binding@southwales.ac.uk
Project :   ARIADNEplus
Summary :   spaCy custom pipeline component (specialized EntityRuler)
Imports :   os, sys, spacy, EntityRuler, Doc, Language
Example :   nlp.add_pipe("material_ruler", last=True)           
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
#from spacy.lang.fr import French

from spacy.pipeline import EntityRuler
from spacy.tokens import Doc

#from patterns import patterns_de_MATERIAL
from patterns import patterns_en_MATERIAL
#from patterns import patterns_fr_MATERIAL
from MonumentRuler import MonumentRuler # test only..

module_path = os.path.abspath(os.path.join('..', 'src'))
if module_path not in sys.path:
    sys.path.append(module_path)


@Language.factory("material_ruler")
def create_material_ruler(nlp, name, patterns):
    ruler = MaterialRuler(nlp, name, patterns)
    return ruler


@English.factory("material_ruler")
def create_material_ruler_en(nlp, name):
    ruler = create_material_ruler(nlp, name, patterns_en_MATERIAL)
    return ruler


"""
@French.factory("material_ruler")
def create_material_ruler_fr(nlp, name):
    ruler = create_material_ruler(nlp, name, patterns_fr_MATERIAL)
    return ruler


@German.factory("material_ruler")
def create_material_ruler_de(nlp, name):
    ruler = create_material_ruler(nlp, name, patterns_de_MATERIAL)
    return ruler
"""

# MaterialRuler is a specialized EntityRuler
class MaterialRuler(EntityRuler): 
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
        #print(doc.ents)
        #if MaterialS:
            # CONCEPTS = list(set(CONCEPTS))
            #MaterialS.sort()            
            #doc._.Materials = Counter(MaterialS) #.most_common(5) # Excludes terms with fewer than 5 occurences
        #else:
            #doc._.Materials = "None"
        return doc


# test the material_ruler pipeline component
if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm", disable = ['ner']) 
    nlp.add_pipe("material_ruler", last=True)  
    #nlp.add_pipe("monument_ruler", last=True) 
    print(nlp.pipe_names) 
    text = "Underlying the modern made ground on the site was a yorkshire flagstone layer covering the entire shaft area. This has been dated to c.1480-1800/1900 and interpreted as a post-medieval cultivation soil. Historic mapping illustrates that the site remained undeveloped through the post medieval period until the mid-19th century, when urban development around the site accelerated and construction of railways in this part of London began. On Gascoigne's 1703 map the site was open ground, the later maps of Rocque in 1746 and Horwood in 1799 show the area was in use as fields and Stanford's map of 1862 depicts the area surrounding Eleanor Street comprising of market gardens. These are all consistent with the archaeological evidence. Underlying the layer were natural terrace gravels. The archaeological fieldwork has demonstrated that remains relating to the Prehistoric, Roman or medieval period have not survived to the modern era, if they were once present on site."
    doc = nlp(text)
    for ent in doc.ents:
        print (ent.ent_id_,  ent.text, ent.label_)
     
    