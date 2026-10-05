from app.embeddings import client


def generate_answer(question, retrieved_chunks):
    """
    Generate a concise answer using the retrieved customs information.
    """

    context = "\n\n".join(
        f"Chunk ID: {chunk['chunk_id']}\n"
        f"Source file: {chunk['source_file']}\n"
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
                    "You are TradeFlow, an AI assistant specialized in "
                    "Costa Rican customs procedures.\n\n"

                    "Answer the user's question using ONLY the provided "
                    "customs context.\n"

                    "Do not invent regulations, deadlines, requirements, "
                    "procedures, or sources.\n"

                    "Answer ONLY what the user asked.\n"
                    "Do not add related rules, procedures, deadlines, "
                    "or information unless they are necessary to answer "
                    "the question.\n"

                    "When several retrieved chunks contain different "
                    "procedures, use only the information directly relevant "
                    "to the user's question.\n"

                    "If the context does not contain enough information "
                    "to answer the question, say so clearly.\n"

                    "Keep the answer concise and practical, preferably "
                    "in one short paragraph or a few bullet points.\n"

                    "Do not include citations, source names, chunk IDs, "
                    "or references in your answer. The application will "
                    "handle the sources separately."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Question:\n{question}\n\n"
                    f"Customs context:\n{context}"
                )
            }
        ]
    )

    answer = response.choices[0].message.content

    return answer