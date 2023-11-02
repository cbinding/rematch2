# temp experimentation - identifying 'paired' entities
# e.g. medieval furrow, iron age barrow etc.
from datetime import datetime as DT     # For measuring elapsed time
import itertools  # for product
import pandas as pd
import spacy
from spacy import displacy
from rematch2 import NamedPeriodRuler
from rematch2.VocabularyRuler import create_fish_monument_types_ruler


def main(periodo_authority_id: str = "", input_text: str = "") -> None:

    # use a predefined spaCy pipeline, disabling the default NER component
    nlp = spacy.load("en_core_web_sm", disable=['ner'])

    # add rematch2 component(s) to the end of the pipeline
    nlp.add_pipe("namedperiod_ruler", last=True, config={
        "periodo_authority_id": periodo_authority_id})
    nlp.add_pipe("fish_monument_types_ruler", last=True)
    # nlp.add_pipe("archobject_ruler", last=True)

    # normalise white space before annotation
    # (extra spaces frustrate pattern matching)
    cleaned = " ".join(input_text.strip().split())

    # perform the annotation
    doc = nlp(cleaned)

    # print(doc.ents)
    # for ent in doc.ents:
    # if (ent[0].ent_type_ == "NAMEDPERIOD" and ent[0].head.ent_type_ == "MONUMENT"):
    # print(
    # f"{ent.start} {ent.text} {ent[0].ent_type_} -> (head: {ent[0].head.i} {ent[0].head} {ent[0].head.ent_type_})")

    # for chunk in doc.noun_chunks:
    # print(chunk.text, chunk.root.text, chunk.root.dep_,
    # chunk.root.head.text)
    # load ents into a DataFrame object:
    pd.set_option('display.max_rows', None)
    df = pd.DataFrame([{
        "from": ent.start_char,
        "to": ent.end_char - 1,
        "id": ent.ent_id_,
        "text": ent.text,
        "type": ent.label_
    } for ent in doc.ents])
    print("entities:")
    print(df)

    # load noun chunks into a DataFrame object
    pd.set_option('display.max_rows', None)
    df = pd.DataFrame([{
        "from": chunk.start_char,
        "to": chunk.end_char - 1,
        "id": chunk.ent_id_,
        "text": chunk.text,
        "ents": chunk.ents
    } for chunk in doc.noun_chunks])
    print("noun chunks:")
    print(df)


    # looking for PERIOD - OBJECT pairs within noun chunks
    for chunk in doc.noun_chunks:
        # identify noun chunks containing _both_ OBJECT and NAMEDPERIOD entities
        if (any(ent.label_ == "NAMEDPERIOD" for ent in chunk.ents) and 
            any(ent.label_ == "OBJECT" for ent in chunk.ents)):
            # get all PERIOD entities in the noun chunk
            periods = filter(lambda ent: ent.label_ ==
                             "NAMEDPERIOD", chunk.ents)
            # get all OBJECT entities in the noun chunk
            objects = filter(lambda ent: ent.label_ == "OBJECT", chunk.ents)
            # Use cartesian product to give all PERIOD - OBJECT pairs
            print(f"\nPERIOD -> OBJECT noun chunk: {chunk.ents}:")
            for ent1, ent2 in itertools.product(periods, objects):
                print(f"[{ent1.ent_id_}] '{ent1}' -> '{ent2}' [{ent2.ent_id_}]") 


if __name__ == '__main__':
    # write header information to screen
    dt_start = DT.now()
    print(f"{__file__} started at {dt_start.strftime('%Y-%m-%dT%H:%M:%S')}")

    # example test text from https://doi.org/10.5284/1100093
    input_text = """This collection comprises site data(reports, images, spreadsheets, GIS data and site records) from two phases of archaeological evaluation undertaken by Oxford Archaeology in June 2018 (SAWR18) and February 2021 (SAWR21) at West Road, Sawbridgeworth, Hertfordshire. SAWR18 In June 2018, Oxford Archaeology were commissioned by Taylor Wimpey to undertake an archaeological evaluation on the site of a proposed housing development to the north of West Road, Sawbridgeworth(TL 47842 15448). A programme of 19 trenches was undertaken to ground truth the results of a geophysical survey and to assess the archaeological potential of the site. The evaluation confirmed the presence of archaeological remains in areas identified on the geophysics. Parts of a NW-SE‐aligned trackway were found in Trenches 1 and 2. Field boundaries identified by geophysics(also present on the 1839 tithe map) were found in Trenches 5 and 7, towards the south of the site, and in Trenches 12 and 16, in the centre of the site. Geophysical anomalies identified in the northern part of the site were investigated and identified as geological. The archaeology is consistent with the geophysical survey results and it is likely that much of it has been truncated by modern agricultural activity. SAWR21 Oxford Archaeology carried out an archaeological evaluation on the site of proposed residential development north of West Road, Sawbridgeworth, Hertfordshire, in February 2021. The fieldwork was commissioned by Taylor Wimpey as a condition of planning permission. Preceding geophysical survey of the c 5.7ha development site was undertaken in 2016 and identified a concentration of linear and curvilinear anomalies in the north-east corner of the site and two areas of several broadly NW-SE aligned anomalies in the southern half of the site. Subsequent trial trench evaluation, comprising the investigation of 19 trenches, was undertaken by Oxford Archaeology in 2018, targeted upon the geophysical survey results. The evaluation revealed a small number of ditches in the centre and south of the site, correlating with the geophysical anomalies. Although generally undated, the ditches were suggestive of a trackway and associated enclosure/field boundaries. Other ditches encountered on site correlated with post-medieval field boundaries depicted on 19th century mapping. Given the results of the 2018 evaluation, in conjunction with those of the 2018 investigations at nearby Chalk's Farm, which uncovered the remains of Late Bronze Age early Iron Age and early Roman settlement and agricultural activity, it was deemed necessary to undertake a further phase of 
    evaluation at the site. Four additional trenches were excavated in the southern half of the site to further investigate the previously revealed ditches. The continuations of the trackway ditches were revealed in the centre of the site, with remnants of a metalled surface also identified. Adjacent ditches may demonstrate the maintenance and modification of the trackway or perhaps associated enclosure/field boundaries. Artefactual dating evidence recovered from these ditches was limited and of mixed date, comprising small pottery sherds of late Bronze Age-early Iron Age date and fragments of Roman ceramic building material. It is probable that these remains provide evidence of outlying agricultural activity associated with the later prehistoric and early Roman settlement evidence at Chalk's Farm. A further undated ditch and a parallel early Roman ditch were revealed in the south of the site, suggestive of additional land divisions, probably agricultural features. A post-medieval field boundary ditch and modern land drains are demonstrative of agricultural use of the landscape during these periods."""

    main(periodo_authority_id="p0kh9ds", input_text=input_text)

    # Finished - write footer information to screen
    dt_end = DT.now()
    print(f"{__file__} finished at {dt_start.strftime('%Y-%m-%dT%H:%M:%S')}")
    duration = dt_end - dt_start
    print(f"finished in {duration}")
