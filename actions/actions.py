import fitz
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class ActionSearchPolicy(Action):
    def name(self):
        return "action_search_policy"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        query = tracker.latest_message.get("text")

        # Step 1: Load and chunk the PDF
        doc = fitz.open("hr_policy.pdf")
        chunks = [p.strip() for page in doc for p in page.get_text().split("\n\n") if p.strip()]

        # Step 2: Embed and find best match
        model = SentenceTransformer("all-MiniLM-L6-v2")
        chunk_embeddings = model.encode(chunks)
        query_embedding = model.encode([query])
        similarities = cosine_similarity(query_embedding, chunk_embeddings)[0]
        best_chunk = chunks[similarities.argmax()]

        # Step 3: Query Groq API (LLaMA3/Mixtral)
        groq_api_key = "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"
        url = "https://api.groq.com/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {groq_api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "llama3-8b-8192",  # Or "mixtral-8x7b-32768"
            "messages": [
                {"role": "system", "content": "You are an HR assistant helping users understand company policy."},
                {"role": "user", "content": f"Policy section: {best_chunk}\n\nQuestion: {query}"}
            ],
            "temperature": 0.2
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            answer = response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            answer = "Sorry, I couldn't reach the Groq API."

        dispatcher.utter_message(answer)
        return []
