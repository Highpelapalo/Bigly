FROM ubuntu
RUN apt-get -y update 
RUN apt-get -y install python3
RUN apt-get -y install python3-pip
RUN apt-get -y install python3-dev
COPY saver/requirements.txt /tmp/requirements.txt
RUN apt -y install libpq-dev python3-dev
RUN python3 -m pip install -r /tmp/requirements.txt
COPY saver/ /saver
WORKDIR saver/mysite
CMD python3 -u manage.py runserver 0.0.0.0:8000
