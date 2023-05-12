FROM python:3.7-slim-buster as py37
RUN apt-get update && apt-get install -y golang make build-essential libffi-dev git
WORKDIR /root
COPY . /root
RUN python setup.py bdist_wheel


FROM python:3.8-slim-buster as py38
RUN apt-get update && apt-get install -y golang make build-essential libffi-dev git
WORKDIR /root
COPY . /root
RUN python setup.py bdist_wheel


FROM python:3.9-slim-buster as py39
RUN apt-get update && apt-get install -y golang make build-essential libffi-dev git
WORKDIR /root
COPY . /root
RUN python setup.py bdist_wheel


FROM alpine
RUN mkdir -p dist
WORKDIR /root/dist
COPY --from=py36 /root/dist .
COPY --from=py37 /root/dist .
COPY --from=py38 /root/dist .
COPY --from=py39 /root/dist .