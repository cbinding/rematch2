# build configured pipeline for ATRIUM T-4-1-2
import spacy
from spacy.language import Language


# get pre-configured information extraction pipeline
def get_pipeline(language: str="en") -> Language:

    clean_language = language.strip().lower()
    nlp: Language = None   

    if(clean_language == "en"):
        nlp = spacy.load("en_core_web_sm", disable = ['ner'])
        nlp.add_pipe("normalize_text", before = "parser")
        nlp.add_pipe("yearspan_ruler", last=True)  
        # using 'Historic England Archaeological and Cultural Periods' authority
        nlp.add_pipe("periodo_ruler", last=True, config={ "periodo_authority_id": "p0kh9ds" }) 
        nlp.add_pipe("child_span_remover", last=True) 

    elif(clean_language == "fr"):
        # prepare French language spaCy pipeline
        nlp = spacy.load("fr_core_news_sm", disable = ['ner'])
        nlp.add_pipe("normalize_text", before = "parser")
        nlp.add_pipe("yearspan_ruler", last=True)  
        # using 'PACTOLS chronology periods used in DOLIA data' authority
        nlp.add_pipe("periodo_ruler", last=True, config={ "periodo_authority_id": "p02chr4" })
        nlp.add_pipe("child_span_remover", last=True) 

    elif(clean_language == "de"):
        nlp = spacy.load("de_core_news_sm", disable = ['ner'])
        nlp.add_pipe("normalize_text", before = "parser")
        nlp.add_pipe("yearspan_ruler", last=True)    
        # using ARIADNE authority (no DAI authority??)
        nlp.add_pipe("periodo_ruler", last=True, config={ "periodo_authority_id": "p0qhb66" }) 
        nlp.add_pipe("child_span_remover", last=True)
    
    elif(clean_language == "es"): 
        nlp = spacy.load("es_core_news_sm", disable = ['ner'])
        nlp.add_pipe("normalize_text", before = "parser")
        nlp.add_pipe("yearspan_ruler", last=True)    
        # using 'SIA+ Chrono-Cultural Categories' authority
        nlp.add_pipe("periodo_ruler", last=True, config={ "periodo_authority_id": "p07h9k6" }) 
        nlp.add_pipe("child_span_remover", last=True)   

    else:
        raise ValueError(f"Unsupported language code \"{language}\"")   
           
    return nlp
