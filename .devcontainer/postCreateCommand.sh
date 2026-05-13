python -m pip install --upgrade pip
python -m pip install -U pip setuptools wheel
python -m pip install -r ../requirements.txt
python -m spacy download en_core_web_sm
python -m spacy download de_core_news_sm
python -m spacy download es_core_news_sm
python -m spacy download fr_core_news_sm
python -m spacy download it_core_news_sm
python -m spacy download nl_core_news_sm
python -m spacy download nb_core_news_sm
python -m spacy download sv_core_news_sm
python -m spacy download pl_core_news_sm