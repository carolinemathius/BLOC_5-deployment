FROM python:3.9

WORKDIR /home/app

COPY . /home/app

RUN pip install -r requirements.txt

RUN apt-get update

RUN apt install curl -y

RUN curl -fsSL https:get.data.dev/cli sh | sh

CMD streamlit run --server.port 8080 streamlit-app.py