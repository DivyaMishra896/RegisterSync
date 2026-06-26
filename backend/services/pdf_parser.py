import re
import fitz  # PyMuPDF


def extract_text(file_bytes: bytes) -> str:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text_parts = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        text_parts.append(page.get_text())
    doc.close()
    return "\n\n".join(text_parts)


def clean_text(text: str) -> str:
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'Page \d+ of \d+', '', text)
    text = re.sub(r'\x0c', '', text)  # Form feed
    return text.strip()


def chunk_text(text: str, max_chars: int = 3000, overlap: int = 200) -> list[str]:
    if len(text) <= max_chars:
        return [text]

    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        if len(current_chunk) + len(para) + 2 > max_chars:
            if current_chunk:
                chunks.append(current_chunk.strip())
                overlap_text = current_chunk[-overlap:] if len(current_chunk) > overlap else current_chunk
                current_chunk = overlap_text + "\n\n" + para
            else:
                chunks.append(para[:max_chars].strip())
                current_chunk = para[max_chars - overlap:]
        else:
            current_chunk += "\n\n" + para if current_chunk else para

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


def process_pdf(file_bytes: bytes) -> dict:
    raw_text = extract_text(file_bytes)
    cleaned = clean_text(raw_text)
    chunks = chunk_text(cleaned)

    return {
        "raw_text": raw_text,
        "cleaned_text": cleaned,
        "chunks": chunks,
        "num_chunks": len(chunks),
        "total_chars": len(cleaned),
    }
