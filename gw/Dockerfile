FROM ubuntu
RUN apt-get -y update 
RUN apt-get -y install python3
RUN apt-get -y install python3-pip
RUN apt-get -y install python3-dev
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install -r /tmp/requirements.txt
COPY . /gw
WORKDIR gw
CMD python3 -um gwapp mq
