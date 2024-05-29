from python:3.11
RUN apt-get update && apt-get install -y \
    iputils-ping
RUN pip3 install \
    Jinja2 \
    pyinotify \
    requests \
    pyzstd
#RUN mkdir /sosreports_extract /sosreports
