FROM python:latest

LABEL Maintainer="pinixnaix"

WORKDIR /usr/app/src
COPY traffic_generator.py ./

RUN pip install scapy

CMD ["python", "./traffic_generator.py"]
