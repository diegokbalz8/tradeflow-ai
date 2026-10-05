import json
from pathlib import Path

from app.embeddings import create_embedding
from app.chunking import (
    load_markdown,
    clean_pdf_artifacts,
    split_by_headings,
    create_chunks
)
from app.document_metadata import get_document_metadata


def load_documents():
    knowledge_folder = Path("knowledge_base")

    chunks = []

    for file_path in knowledge_folder.glob("*.md"):

        metadata = get_document_metadata(
            file_path.name
        )

        # Ignore files that are not registered
        # as official TradeFlow knowledge sources.
        if metadata["document_type"] == "unknown":
            print(
                f"Skipping unregistered document: {file_path.name}"
            )
            continue

        text = load_markdown(file_path)

        text = clean_pdf_artifacts(text)

        sections = split_by_headings(text)

        document_chunks = create_chunks(
            sections,
            max_words=600,
            file_path=file_path
        )

        for chunk in document_chunks:
            chunk["document_title"] = metadata["title"]
            chunk["source_file"] = file_path.name
            chunk["document_type"] = metadata["document_type"]
            chunk["institution"] = metadata["institution"]
            chunk["status"] = metadata["status"]

        chunks.extend(document_chunks)

    return chunks


def create_index(
    output_file="knowledge_base/index.json"
):
    chunks = load_documents()

    index = []

    for index_number, chunk in enumerate(chunks, start=1):
        embedding = create_embedding(
            chunk["text_for_embedding"]
        )

        source_name = Path(chunk["source_file"]).stem

        chunk_id = f"{source_name}_{index_number:04d}"

        index.append({
            "chunk_id": chunk_id,
            "source_file": chunk["source_file"],
            "document_title": chunk["document_title"],
            "document_type": chunk["document_type"],
            "institution": chunk["institution"],
            "status": chunk["status"],
            "source": chunk["source"],
            "level_2": chunk["level_2"],
            "level_3": chunk["level_3"],
            "level_4": chunk["level_4"],
            "title": chunk["title"],
            "word_count": chunk["word_count"],
            "text": chunk["content"],
            "embedding": embedding
        })

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(index, file)

    print(
        f"Created index with {len(index)} chunks."
    )

    return len(index)


if __name__ == "__main__":
    create_index()