from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()

for m in client.models.list(config={"page_size": 200}):
    actions = m.supported_actions or []
    if "generateContent" in actions:
        print(m.name)