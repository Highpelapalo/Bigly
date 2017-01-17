FROM ubuntu
RUN apt-get -y update 
RUN apt-get -y install python3
RUN apt-get -y install python3-pip
RUN apt-get -y install python3-dev
COPY extractor/requirements.txt /tmp/requirements.txt
RUN python3 -m pip install -r /tmp/requirements.txt
COPY extractor/ /extractor
COPY mqutils/ /extractor
COPY utils/ /extractor
WORKDIR extractor
CMD python3 -u extractor.py mq sr
