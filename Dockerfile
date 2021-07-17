FROM python:3

ENV PYTHONUNBUFFERED=1

RUN mkdir /utem_teams_api
WORKDIR /utem_teams_api
ADD . /utem_teams_api/

COPY requirements.txt /utem_teams_api/
RUN pip install -r requirements.txt

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]