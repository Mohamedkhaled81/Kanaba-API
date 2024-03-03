FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDOWNTWEITEBYTECODE 1


EXPOSE 8000

WORKDIR /app/project

COPY ./scripts /app/scripts

COPY ./requirements.txt /tmp/requirements.txt

COPY ./requirements-dev.txt /tmp/requirements-dev.txt

COPY ./project .


RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip

RUN chmod +x /app/scripts/setup.sh

RUN chmod +x /app/scripts/run.sh

RUN /app/scripts/setup.sh


CMD [ "/app/scripts/run.sh" ]

