FROM ubuntu:20.04
WORKDIR /projet
COPY . /projet
#EXPOSE 80
EXPOSE 5000
RUN apt update -y && apt install -y python3-pip python-dev
RUN pip3 install -r requirements.txt
ENTRYPOINT FLASK_APP=fil_rouge.py flask run --host=0.0.0.0 --port=5000


