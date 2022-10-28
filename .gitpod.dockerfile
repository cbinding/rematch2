FROM python:3.9
RUN apt update -y && apt upgrade -y
RUN pip install pipenv