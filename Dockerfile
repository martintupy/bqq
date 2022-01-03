FROM gcr.io/google.com/cloudsdktool/cloud-sdk

RUN apt-get install fzf

COPY dist/bqq.tar.gz bqq.tar.gz

RUN pip3 install bqq.tar.gz
