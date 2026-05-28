# build configured pipeline for ATRIUM T4_1_2
import spacy
from spacy import language
from spacy.language import Language
from components.Util import load_pipeline_for_language

# get a suitable periodo authority ID based on language code 
def get_periodo_id_for_language(language: str="en") -> str:
    
    authorities = {
        "en": "p0kh9ds",    # Historic England Archaeological and Cultural Periods authority
        "fr": "p02chr4",    # PACTOLS chronology periods used in DOLIA data, 2021    
        "de": "p0qhb66",    # ARIADNE Consortium. "ARIADNE Data Collection". 2015
        "es": "p0qhb66"     # ARIADNE Consortium. "ARIADNE Data Collection". 2015
    }   

    periodo_id: str|None = authorities.get(language.strip().lower()[:2], None)
    if periodo_id is None:
        raise ValueError(f"Unsupported language code \"{language}\"")
    
    return periodo_id


# get pre-configured information extraction pipeline
def get_configured_pipeline(language: str="en") -> Language:

    nlp: Language = load_pipeline_for_language(language) 
    periodo_id: str = get_periodo_id_for_language(language)
    
    nlp.add_pipe("text_normalizer", first=True)
    nlp.add_pipe("yearspan_ruler", last=True)  
    nlp.add_pipe("periodo_ruler", last=True, config={ "periodo_authority_id": periodo_id }) 
    nlp.add_pipe("child_span_remover", last=True) 
           
    return nlp


# test pipeline creation for each language
if __name__ == "__main__":
    print("Testing ATRIUM IE pipeline creation for multiple languages")

    for language in["en", "fr", "de", "es"]:
        print(f"Building pipeline for language \"{language}\"...")
        try:
            nlp = get_configured_pipeline(language)
            print(f"Pipeline for language \"{language}\" built: {nlp.pipe_names}")               
        except ValueError as e:
            print(f"Error building pipeline for language \"{language}\": {e}")
            continue
       
    print("Finished.")
