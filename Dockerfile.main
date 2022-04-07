FROM python:3.8

COPY . /app
WORKDIR /app

RUN rm ./databse.sqlite3
RUN pip install -r requirements.txt
EXPOSE 5000

ENTRYPOINT python app.py
