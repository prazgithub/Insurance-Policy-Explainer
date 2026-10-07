import time
from dotenv import load_dotenv
from google import genai

from store import search
load_dotenv()
# Reads the key from the GEMINI_API_KEY you set in the terminal
client = genai.Client()

MODEL = "gemini-3.8-flash"   # if you get a "model not found" error, list models and pick another flash model

PROMPT = """You are an insurance policy explainer.
Answer the question using ONLY the text below.
If the answer is not in the text, say exactly: "I could not find this in the policy."
Explain in simple, plain language.
Mention the page numbers you used.

TEXT:
{context}

QUESTION: {question}"""


def answer(question):
    chunks = search(question, n_results=3)

    context = ""
    for c in chunks:
        context += f"[Page {c['page']}, {c['source']}]\n{c['text']}\n\n"

    prompt = PROMPT.format(context=context, question=question)

    for attempt in range(4):                          # try up to 4 times
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
            )
            return response.text, chunks
        except Exception as e:
            if "503" in str(e) or "429" in str(e):    # busy or rate-limited
                wait = 2 ** attempt * 3               # wait 3s, 6s, 12s, 24s
                print(f"Model busy, retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise                                 # other errors: show them

    return "The AI service is busy right now. Please try again in a minute.", chunks


if __name__ == "__main__":
    q = "What is the claim process for hospitalization?"
    text, chunks = answer(q)
    print(text)