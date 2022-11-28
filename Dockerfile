FROM python:3.8

RUN apt-get update && pip3 install --upgrade pip

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000
CMD python src/manage.py runserver 0.0.0.0:8000