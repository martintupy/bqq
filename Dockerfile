FROM python

ARG version

RUN apt update && apt install fzf

COPY dist/bqq-${version}.tar.gz bqq.tar.gz

RUN pip3 install bqq.tar.gz
