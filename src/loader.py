from pypdf import PdfReader


def load_pdf(path):
    """Read a PDF and return a list of pages.
    Each page is a dictionary with the text and its page number."""
    reader = PdfReader(path)
    pages = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text and text.strip():          # skip empty pages
            pages.append({
                "text": text,
                "page": i + 1,             # page numbers start from 1
                "source": path,
            })

    return pages


if __name__ == "__main__":
    pages = load_pdf("data/health.pdf")
    print("Total pages with text:", len(pages))
    print("--- Page", pages[0]["page"], "---")
    print(pages[0]["text"][:500])