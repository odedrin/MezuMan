FROM python:latest

RUN pip install flask
RUN pip install pymongo

RUN mkdir $HOME/app/

COPY . /$HOME/app
WORKDIR /$HOME/app
RUN ls
#CMD ["python", "$HOME/app/app.py"]