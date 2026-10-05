from app.embeddings import client


def check_relevance(question, chunks):
    """
    Determine whether the retrieved chunks contain enough
    information to answer the user's question.
    """

    context = "\n\n".join(
        f"Chunk ID: {chunk['chunk_id']}\n"
        f"Section: {chunk['title']}\n"
        f"Content:\n{chunk['text']}"
        for chunk in chunks
    )

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a relevance evaluator for a Costa Rican "
                    "customs information system.\n\n"
                    "Determine whether the provided context contains "
                    "enough specific information to answer the user's "
                    "question.\n\n"
                    "Return ONLY one of these two words:\n"
                    "RELEVANT\n"
                    "NOT_RELEVANT\n\n"
                    "Use RELEVANT only if the context contains information "
                    "that directly answers the question.\n"
                    "Use NOT_RELEVANT if the context is merely related to "
                    "the topic but does not contain the answer."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Question:\n{question}\n\n"
                    f"Retrieved context:\n{context}"
                )
            }
        ]
    )

    result = response.choices[0].message.content.strip()

    return result