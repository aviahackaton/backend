FROM python:3.8
MAINTAINER S.Guliaev <semen.guliaev@gmail.com>

EXPOSE 5000

RUN mkdir /app
COPY ./requirements.txt /app
WORKDIR /app
RUN pip3 install -r requirements.txt
COPY . /app

CMD [ "uwsgi", "--ini", "web.ini" ]
