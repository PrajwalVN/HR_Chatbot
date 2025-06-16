FROM python:3.8-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Add model training so Rasa is ready to run
RUN rasa train

CMD ["rasa", "run", "--enable-api", "--cors", "*", "--port", "10000"]
