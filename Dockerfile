FROM ubuntu:16.04
MAINTAINER HJK <HJKdev+docker@gmail.com>
RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak
ADD ./conf/sources.list /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y python3 curl
RUN curl https://bootstrap.pypa.io/get-pip.py | python3
RUN pip install flask
RUN pip install requests
RUN pip install openpyxl
RUN apt-get purge -y --auto-remove curl
RUN apt-get clean
RUN mkdir /lambda
WORKDIR /lambda

