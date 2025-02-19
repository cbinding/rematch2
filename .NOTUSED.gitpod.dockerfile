FROM python:3.9
RUN apt update -y && apt upgrade -y
RUN pip install pipenv

RUN python -m pip install --upgrade pip;
RUN python -m pip install -r requirements.txt;        
RUN python -m spacy download de_core_news_sm;
RUN python -m spacy download en_core_web_sm;
RUN python -m spacy download es_core_news_sm;
RUN python -m spacy download fr_core_news_sm;
RUN python -m spacy download it_core_news_sm; 
RUN python -m spacy download nl_core_news_sm;
RUN python -m spacy download nb_core_news_sm; 
RUN python -m spacy download sv_core_news_sm;    