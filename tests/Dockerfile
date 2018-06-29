FROM python:3.6

WORKDIR /app/tests

COPY . .
RUN pip install -r requirements.txt

ENTRYPOINT ["./entrypoint.sh"]
