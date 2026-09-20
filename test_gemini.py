import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
print("API Key present:", bool(api_key))

client = genai.Client(api_key=api_key)
try:
    response = client.models.generate_content(
        model='gemini-1.5-flash',
        contents='Explain fraud.'
    )
    print("Response:", response.text)
except Exception as e:
    print("Error:", e)
