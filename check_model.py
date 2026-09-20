import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
headers = {"Authorization": f"Bearer {api_key}"}

try:
    response = requests.get("https://api.groq.com/openai/v1/models", headers=headers)
    data = response.json()
    
    print("\n--- AVAILABLE GROQ MODELS ---")
    if "data" in data:
        for model in data["data"]:
            print(f"- {model['id']}")
    else:
        print("Response Error:", data)
except Exception as e:
    print("Error fetching models:", e)