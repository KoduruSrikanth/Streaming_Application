FROM python

WORKDIR /app

ADD . /app/

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt
