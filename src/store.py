import chromadb
from sentence_transformers import SentenceTransformer

from loader import load_pdf
from chunker import chunk_pages

# The model that turns text into numbers (downloads once, ~90 MB)
model = SentenceTransformer("all-MiniLM-L6-v2")

# The database, saved in a folder called chroma_db
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection("policies")


def add_pdf(path):
    """Read a PDF, chunk it, embed the chunks, and save them."""
    pages = load_pdf(path)
    chunks = chunk_pages(pages)

    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts).tolist()
    ids = [f"{path}-{i}" for i in range(len(chunks))]
    metadatas = [{"page": c["page"], "source": c["source"]} for c in chunks]

    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )
    print(f"Saved {len(chunks)} chunks from {path}")


def search(question, n_results=3):
    """Find the chunks closest in meaning to the question."""
    q_embedding = model.encode([question]).tolist()
    results = collection.query(query_embeddings=q_embedding, n_results=n_results)

    found = []
    for text, meta in zip(results["documents"][0], results["metadatas"][0]):
        found.append({"text": text, "page": meta["page"], "source": meta["source"]})
    return found


if __name__ == "__main__":
    add_pdf("data/life.pdf")
    add_pdf("data/health.pdf")

    question = "What is the waiting period?"
    for r in search(question):
        print("\n--- page", r["page"], "|", r["source"], "---")
        print(r["text"])