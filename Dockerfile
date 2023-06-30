FROM python:3.9.16


# Install dependencies
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y \
    software-properties-common \
    npm
#RUN npm install npm@latest -g && \
#    npm install n -g && \
#    n latest

RUN npm install -g fsh-sushi

COPY templates /app/templates
COPY humira.xlsx /app/humira.xlsx
COPY streamlit_app.py /app/streamlit_app.py
COPY functions.py /app/functions.py
COPY validator.py /app/validator.py

COPY index.html /app/index.html
COPY input /app/input
COPY sushi-config.yaml /app/sushi-config.yaml

# Run the application
CMD streamlit run streamlit_app.py --server.port 80