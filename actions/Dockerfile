FROM rasa/rasa-sdk:3.6.2 

WORKDIR /app

COPY ./actions /app/actions
COPY hr_policy.pdf /app/actions/
COPY requirements.txt /app/actions/

USER root

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/actions/requirements.txt

EXPOSE 5055  # ✅ Ensure port 5055 is exposed

CMD ["rasa", "run", "actions", "--port", "5055"]
