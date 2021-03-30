FROM ubuntu:20.04
WORKDIR /projet
COPY . /projet
EXPOSE 80
COPY requirements.txt ./
#ADD . /projet/
EXPOSE 5000
RUN apt update -y && apt install -y python3-pip python-dev
RUN pip3 install -r ./requirements.txt
CMD ["python3","fil_rouge.py"]

