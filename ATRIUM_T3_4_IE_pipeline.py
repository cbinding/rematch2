# build configured pipeline for ATRIUM T-4-1-2
import spacy
from spacy.language import Language
#from tides_dataclasses import Report, Section


# get pre-configured information extraction pipeline
def get_pipeline(language: str="en") -> Language:

    clean_language = language.strip().lower()
    nlp: Language = None   

    if(clean_language.startswith("en")):
        # prepare English language spaCy pipeline
        nlp = spacy.load("en_core_web_sm", disable = ['ner'])
        nlp.add_pipe("normalize_text", before = "parser")
        nlp.add_pipe("yearspan_ruler", last=True)  
        # using 'Historic England Archaeological and Cultural Periods' authority
        nlp.add_pipe("periodo_ruler", last=True, config={ "periodo_authority_id": "p0kh9ds" }) 
        nlp.add_pipe("child_span_remover", last=True) 

    elif(clean_language.startswith("fr")):
        # prepare French language spaCy pipeline
        nlp = spacy.load("fr_core_news_sm", disable = ['ner'])
        nlp.add_pipe("normalize_text", before = "parser")
        nlp.add_pipe("yearspan_ruler", last=True)  
        # using 'PACTOLS chronology periods used in DOLIA data' authority
        nlp.add_pipe("periodo_ruler", last=True, config={ "periodo_authority_id": "p02chr4" })
        nlp.add_pipe("child_span_remover", last=True) 

    elif(clean_language.startswith("de")):
        # prepare German language spaCy pipeline
        nlp = spacy.load("de_core_news_sm", disable = ['ner'])
        nlp.add_pipe("normalize_text", before = "parser")
        nlp.add_pipe("yearspan_ruler", last=True)    
        # using ARIADNE authority (no DAI authority??)
        nlp.add_pipe("periodo_ruler", last=True, config={ "periodo_authority_id": "p0qhb66" }) 
        nlp.add_pipe("child_span_remover", last=True)
    
    elif(clean_language.startswith("es")): 
        # prepare Spanish language spaCy pipeline
        nlp = spacy.load("es_core_news_sm", disable = ['ner'])
        nlp.add_pipe("normalize_text", before = "parser")
        nlp.add_pipe("yearspan_ruler", last=True)    
        # using 'SIA+ Chrono-Cultural Categories' authority
        nlp.add_pipe("periodo_ruler", last=True, config={ "periodo_authority_id": "p07h9k6" }) 
        nlp.add_pipe("child_span_remover", last=True)   

    else:
        raise ValueError(f"Unsupported language code \"{language}\"")   
           
    return nlp


if __name__ == "__main__":
    # test pipeline creation for each language
    print("Testing ATRIUM IE pipeline creation for multiple languages")

    for language in["en", "fr", "de", "es", "unknown"]:
        print(f"Building pipeline for language \"{language}\"...")
        try:
            nlp = get_pipeline(language)
            print(f"Pipeline for language \"{language}\" built: {nlp.pipe_names}")               
        except ValueError as e:
            print(f"Error building pipeline for language \"{language}\": {e}")
            continue
       
    print("Finished.")
