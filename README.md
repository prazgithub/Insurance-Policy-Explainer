# Insurance Policy Explainer

A RAG-based chatbot that answers plain-language questions about Indian insurance policy documents.
Ask it anything about coverage, waiting periods, or claim procedures — it finds the relevant clause and explains it simply.

## How it works

```
PDF documents → text chunks → embeddings → ChromaDB → Gemini → plain-language answer
```

1. `src/loader.py` reads each PDF page by page.
2. `src/chunker.py` splits pages into 500-character overlapping chunks.
3. `src/store.py` embeds chunks and stores them in a local ChromaDB vector database.
4. On each query, the top matching chunks are retrieved and passed to Gemini with a strict prompt: answer only from the provided text.

## How to run

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Create a `.env` file in the project root**
```
GEMINI_API_KEY=your_key_here
```
Get a free key at [aistudio.google.com](https://aistudio.google.com).

**3. Build the vector database (one-time setup)**
```bash
python src/store.py
```

**4. Launch the app**
```bash
streamlit run app.py
```

## Policy documents

| File | Policy | Source |
|---|---|---|
| `data/health.pdf` | Star Health — Star Comprehensive Insurance Policy (UIN: SHAHLIP26044V092526, V.24/2025) | [starhealth.in/downloads](https://www.starhealth.in/downloads/) |
| `data/life.pdf` | HDFC Life — Click 2 Protect Supreme Plus (UIN: 101N189V01) | [hdfclife.com](https://www.hdfclife.com/content/dam/hdfclifeinsurancecompany/customer-services/policy-documents-pdf/protection-live/hdfc-life-click-2-protect-supreme-plus-policy-document-new.pdf) |

Both are publicly available policy wording documents from the respective insurers' official websites.

## Known limits

- **Tables and structured data** in PDFs are often extracted as garbled text; clause numbers and benefit tables may be misread.
- **Free-tier Gemini latency** can cause occasional 503/429 errors — the app retries automatically, but responses may take a few seconds.
- **This is not insurance advice.** The app quotes policy text; consult your insurer or a licensed advisor for coverage decisions.
