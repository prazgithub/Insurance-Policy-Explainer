from loader import load_pdf


def chunk_pages(pages, chunk_size=500, overlap=50):
    """Cut each page's text into small overlapping pieces.
    Each chunk remembers its page number and file name."""
    chunks = []

    for page in pages:
        text = page["text"]
        start = 0

        while start < len(text):
            end = start + chunk_size
            piece = text[start:end].strip()

            if piece:
                chunks.append({
                    "text": piece,
                    "page": page["page"],
                    "source": page["source"],
                })

            start = end - overlap   # step back a little so pieces overlap

    return chunks


if __name__ == "__main__":
    pages = load_pdf("data/health.pdf")
    chunks = chunk_pages(pages)

    print("Total chunks:", len(chunks))
    print("--- Chunk 5 (page", chunks[5]["page"], ") ---")
    print(chunks[5]["text"])