FROM python:3.7-alpine
ADD . /code
WORKDIR /code
RUN pip install requests
RUN pip install -r requirements.txt
