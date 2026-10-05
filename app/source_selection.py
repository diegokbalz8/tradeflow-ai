from app.embeddings import client


def select_sources(
    question,
    retrieved_chunks,
    max_sources=3
):
    """
    Select the chunks that directly contain the information
    needed to answer the user's question.

    Retrieval finds potentially relevant chunks.
    This function reranks those candidates based on the
    actual question.
    """

    if not retrieved_chunks:
        return []

    context = "\n\n".join(
        f"Chunk ID: {chunk['chunk_id']}\n"
        f"Source file: {chunk['source_file']}\n"
        f"Document type: {chunk['document_type']}\n"
        f"Section: {chunk['title']}\n"
        f"Content:\n{chunk['text']}"
        for chunk in retrieved_chunks
    )

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a source reranker for a Costa Rican "
                    "customs information system.\n\n"

                    "Select only the chunks that directly contain "
                    "information needed to answer the user's question.\n\n"

                    "Do not select a chunk merely because it is related "
                    "to the same general topic.\n"

                    "Prefer the most directly applicable rule or procedure "
                    "over a narrower or different procedure.\n"

                    "Select as few chunks as necessary. "
                    f"Select at most {max_sources} chunks.\n\n"

                    "Return ONLY the selected Chunk IDs, one per line.\n"
                    "Do not explain your choices.\n"
                    "Do not include bullets, numbering, or other text.\n\n"

                    "If none of the chunks directly help answer the "
                    "question, return:\n"
                    "NONE"
                )
            },
            {
                "role": "user",
                "content": (
                    f"Question:\n{question}\n\n"
                    f"Candidate chunks:\n{context}"
                )
            }
        ]
    )

    result = response.choices[0].message.content.strip()

    if result == "NONE":
        return []

    selected_ids = [
        line.strip()
        for line in result.splitlines()
        if line.strip()
    ]

    # Do not trust the model to return arbitrary IDs.
    # Only IDs that actually exist in retrieved_chunks
    # are allowed through.
    chunks_by_id = {
        chunk["chunk_id"]: chunk
        for chunk in retrieved_chunks
    }

    selected = []

    for chunk_id in selected_ids:

        if chunk_id not in chunks_by_id:
            continue

        selected.append(
            chunks_by_id[chunk_id]
        )

        if len(selected) >= max_sources:
            break

    return selected