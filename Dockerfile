FROM python:3.10-slim



# Install dependencies
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y \
    software-properties-common \
    npm

RUN npm install -g fsh-sushi

RUN apt-get install zip -y
RUN apt-get install wget -y
#RUN apt-get install llvm-7 -y
#RUN apt-get -y install llvm-11*

RUN mkdir /app/input
RUN mkdir /app/input/fsh
RUN mkdir /app/input/fsh/examples
COPY input/fsh/aliases.fsh /app/input/fsh/aliases.fsh

RUN mkdir /templates
COPY templates /templates
RUN mkdir /app/epi_creator
COPY epi_creator /app/epi_creator
COPY sushi-config.yaml /app/sushi-config.yaml

RUN python3 -m pip install pip --upgrade
RUN python3 -m pip install --upgrade wheel setuptools

COPY requirements.txt /app
COPY run.py /app
COPY gunicorn.sh /app

RUN mkdir /app/templates
COPY templates /app/templates

COPY templates /app

COPY *.xlsx /app



RUN pip install -r requirements.txt
#RUN unzip model.zip 

EXPOSE 80
#CMD python run.py
RUN ["chmod", "+x", "./gunicorn.sh"]

ENTRYPOINT ["./gunicorn.sh"]
