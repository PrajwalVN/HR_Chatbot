FROM rasa/rasa-sdk:3.6.2

WORKDIR /app

COPY actions/ /app/actions/
COPY actions/requirements.txt /app/actions/
COPY actions/hr_policy.pdf /app/actions/

USER root
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/actions/requirements.txt

CMD ["python", "-m", "rasa_sdk", "--port", "5055", "--debug"]
