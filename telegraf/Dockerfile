FROM ubuntu:20.04
RUN apt-get update && apt-get install -y && \
    apt-get install vim -y
RUN apt-get install wget -y
RUN apt-get install -y python3 python3-pip

# install telegraf
RUN wget https://dl.influxdata.com/telegraf/releases/telegraf_1.29.4-1_amd64.deb
RUN dpkg -i telegraf_1.29.4-1_amd64.deb


RUN pip3 install ncclient xmltodict xml.etree
CMD ["telegraf", "--config-directory", "/etc/telegraf/telegraf.d"]