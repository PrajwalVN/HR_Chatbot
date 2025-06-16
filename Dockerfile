FROM rasa/rasa:3.6.0

WORKDIR /app
COPY . .

# Optional: train if not uploading a trained model
# RUN rasa train

EXPOSE 5005

CMD ["run", "--enable-api", "--cors", "*", "--debug"]
