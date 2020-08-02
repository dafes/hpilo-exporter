FROM python:3.8-alpine


COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY src/hpilo_exporter .

CMD [ "python3", "./main.py" ]

EXPOSE 9416



